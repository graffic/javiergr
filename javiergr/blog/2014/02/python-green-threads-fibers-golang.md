title: Python, green threads, fibers and go
date: 2014-02-09
category: technical
published: true
summary: The go language concurrency model and python.

The [Go language concurrency model][golang-concurrency] [isn't
new][actor-model]. Somehow it has caught my eye how easy is to use and write
concurrent code using channels and lightweight threads ([actors][actor-model]).

But there are different kinds of threads:

- *Thread*: Instructions scheduled by the operating system.
- *Green Thread*: Scheduled by the language virtual machine. Usually lighter.
- *Fiber*: Coroutines, scheduled cooperatively.
- *Coroutine*: a subroutine (method, function) that can be suspended.

Python has support for all of these. I'd like to focus on green threads and fibers.
Let's start with two examples in go.

## Examples in go

The *first* one I call it `gophers`. It's taken from a go tutorial. The idea is
that many goroutines (like green threads) exchange messages. Each one send to
the next the value it receives from the previous goroutine plus one. 

If you're new to the actor model, see how there are no callbacks just threads blocking for content
from a channel (the `<-` symbol).

    :::go
    package main

    import "fmt"

    func gopher(left, right chan int) {
		left <- 1 + <-right
	}

	func starter(right chan int) {
		right <- 1
	}

	func main() {
		const n = 100000
		leftmost := make(chan int)
		right := leftmost
		left := leftmost
		for i := 0; i < n; i++ {
			right = make(chan int)
			go gopher(left, right)
			left = right
		}

		go starter(right)
		fmt.Println(<-leftmost)
	}

The *second* example adds `IO` to the mix. It watches the output of two tail
commands and prints their output. Again the *goroutines* just block waiting for
content and the main loop blocks waiting for their messages in the channel.

    :::go
	package main

	import (
		"fmt"
		"os/exec")

	func my_tail(output chan string, filename string) {
		cmd := exec.Command("tail", "-f", filename)
		stdout, err := cmd.StdoutPipe()
		if (err != nil) {
			return
		}
		if err := cmd.Start(); err != nil {
			return
		}
		buf := make([]byte, 1024)
		for {
			n, err := stdout.Read(buf)
			if n != 0 {
				output <- string(buf[:n])
			}
			if err != nil {
				break
			}
		}
	}

	func main() {
		ch := make(chan string)
		go my_tail(ch, "f1.txt")
		go my_tail(ch, "f2.txt")

		for {
			text := <-ch
			fmt.Print(text)
		}
	}

## Gophers in python

The first example is my favorite for [Stackless Python][stackless-python]. It shows how powerful
and fast it can be.

    :::python
	from stackless import channel, tasklet

	def gopher(left, right):
    	left.send(right.receive() + 1)

	def starter(chan):
    	chan.send(1)

	if __name__ == "__main__":
    	leftmost = channel()
    	right = leftmost
    	left = leftmost
    	for _ in range(1000000):
        	right = channel()
        	tasklet(gopher)(left, right)
        	left = right
    	tasklet(starter)(right)
    	print(leftmost.receive())	

You can run one million of green threads quite fast (4s in my machine). I might
add that it can do that faster than go (17s), but it won't make any justice to
Go, just show a strong point of stackless python.

With [gevent][gevent] the code is almost the same. Unfortunately it's much
slower (87s).

	:::python
	from gevent.queue import Channel
	import gevent

	def gopher(left, right):
    	left.put(right.get() + 1)

	def starter(chan):
    	chan.put(1)

	if __name__ == "__main__":
    	leftmost = Channel()
    	right = leftmost
    	left = leftmost
    	for _ in xrange(1000000):
        	right = Channel()
        	gevent.spawn(gopher, left, right)
        	left = right
    	gevent.spawn(starter, right)
    	print(leftmost.get())

Using [python fibers][python-fibers] through the [offset
library][offset-library] wasn't a very successful experiment. I was able to
create only 1512 fibers (well, task wrapped in fibers). With more than that I
was rewarded with a `segmentation fault`.

	:::python
	from offset import maintask, run, go, makechan

	def gopher(left, right):
    	left.send(right.recv() + 1)

	def starter(chan):
    	chan.send(1)

	@maintask
	def main():
    	leftmost = makechan()
    	right = leftmost
    	left = leftmost
    	for _ in range(1511):
        	right = makechan()
        	go(gopher, left, right)
        	left = right
    	go(starter, right)
    	print(leftmost.recv())

	if __name__ == "__main__":
    	run()

## Adding IO

The problem with the actor approach in python is that you have to make it
explicit. In the previous examples there was code there to send messages and
wait for them. If we add IO, we will need specific IO code for each library, or
monkey patch the existing one.

In stackless python I found only one library for non-blocking IO: [syncless][syncless]. It didn't work very well :(

- Didn't compile in stackless python 3.3 so I switched to 2.7
- Monkey patching for subprocess and popen didn't work.
- Got random crashes.

Gevent seems to be up to date and handled the example without any problem.

	:::python
	from gevent.subprocess import Popen, PIPE
	from gevent.queue import Channel
	import gevent

	def tail(output, filename):
    	proc = Popen(["tail", "-f", filename], stdout=PIPE)
    	while True:
        	output.put(proc.stdout.readline().strip())

	if __name__ == "__main__":
    	output = Channel()
    	gevent.spawn(tail, output, "f1.txt")
    	gevent.spawn(tail, output, "f2.txt")
    	while True:
        	print output.get()

And last but not least, the offset & fibers combo. It has basic socket and file support,
but I couldn't find how to patch popen or subprocess (or a patched version).

## Summary

[Gevent][gevent] seems to have all the good parts of the green threads model.
I'd like to see stackless with a better IO library, or learn more about how
[CCP games][ccp-stackless] handles IO in their stackless installation.

And of course, give the [Go programming language][golang] a try.
 

[golang-concurrency]: http://golang.org/doc/effective_go.html#concurrency
[actor-model]: http://en.wikipedia.org/wiki/Actor_model
[stackless-python]: http://www.stackless.com/
[gevent]: http://www.gevent.org/
[python-fibers]: https://python-fibers.readthedocs.org/en/latest/
[offset-library]: https://github.com/benoitc/offset
[syncless]: https://code.google.com/p/syncless/
[subprocess-library]: http://docs.python.org/3.3/library/subprocess.html
[ccp-stackless]: http://www.slideshare.net/Arbow/stackless-python-in-eve
[golang]: http://golang.org

title: Python patching function globals
date: 2014-04-08
category: technical
published: true
summary: Python functions references to globals and monkey patching.

Some days ago I found myself close to [monkey patch][monkeypatch] a global
reference to a method. I wanted to modify the output of an internal method in a
3rd party framework. Even if the framework had hooks, it didn't have the one I
needed.

Monkey patching usually is **not** a good solution.

- Your changes might be global.
- Your changes could have unexpected consequences.
- For sure it can be done in another way.
- You're binding your code to 3rd party internals.

There was only one place where the relevant method was used, and that place
(function) was being stored to be called later. Could I replace that stored
function with one with the *same code* but *different dependencies*?

## Python function references

[Python functions][pythonfunctions] keep a reference to the *non-local*
variables used in the following attributes

- `__globals__` This is a reference to the module globals dict.
- `__closure__` Variables used in the function closure.

Let's see it with an example:

	:::pycon

	>>> def one():
	...     return 'one'
	...
	>>> def three(param):
	...     def two():
	...         print(one(), param)
	...     return two
	...
	>>> inst = three('hello')
	>>> inst()
	('one', 'hello')
	>>> inst.__globals__
	{'__builtins__': <module '__builtin__' (built-in)>, 
 	 'three': <function three at 0x109306cf8>, 
 	 'one': <function one at 0x109306c80>, 
 	 'inst': <function two at 0x109306d70>, 
 	 '__name__': '__main__', 
 	 '__package__': None, 
 	 '__doc__': None}
	>>> inst.__closure__
	(<cell at 0x10930c600: str object at 0x10930b510>,)
	>>> inst.__closure__[0].cell_contents
	'hello'


These two dictionaries aren't read only (the attributes are tough). However, in
the case of the globals dictionary any modification will apply to everyone
using not only the method but the module.

## Copying a method

We can duplicate a method and make it use a new globals dict. For example, in
order to change the reference to the method `one` inside the method `two` to
the `banana` method (using the previous example code):

	:::pycon
	>>> import types
	>>> def banana():
	...     return 'banana'
	...
	>>> new_globals = inst.__globals__.copy()
	>>> new_globals['one'] = banana
	>>> patched_inst = types.FunctionType(
	...     inst.__code__, new_globals, inst.__name__, 
	...     inst.__defaults__, inst.__closure__)
	>>> patched_inst()
	('banana', 'hello')
	>>> inst()
	('one', 'hello')

## Summary

This still is monkey patching, even if no global reference is modified and only
references kept in an instance are changed (no global modifications), like in a
*dict* or a *list*. Although it allows precise surgery in some cases or till
your pull request is accepted in your favorite open source 3rd party dependency.

[monkeypatch]: http://en.wikipedia.org/wiki/Monkey_patch
[pythonfunctions]: https://docs.python.org/3/reference/datamodel.html#index-32

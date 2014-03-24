title: A take on don't repeat yourself
date: 2014-03-22
category: technical
published: true
summary: DRY means yourself and not only code.

“Don't repeat yourself” is a software development principle (big words) that
tells us to avoid repetition of *information of all kinds* in a software
system. It means yourself, but many times it is used only for code.

Some days ago I stumbled upon a [nice article][justinweiss_post] by
[@justinweiss][justinweiss_twitter] about how DRY can go wrong in your code.
Really good examples but only focused on code and leaving aside the *yourself*
part and not using other software development principles to balance the
excessive use of only one. Like the *every problem is a nail when you only have
a hammer* motto. The first two that came to my mind were:

- [Last responsible moment][LRM]
- [Pareto principle][pareto]

But let's start with the Y in DRY.

## Don't repeat yourself - code

*Try to avoid duplication on information of all kinds*. When I look at code as
a bunch of lines, I might see "string duplication", where a bunch of lines of
code are the same in two parts of the application. There are some tools that
will help you to find them (For example pylint in python). But when code is
*information*, that piece of knowledge:

- It might have the same character representation as another piece of totally
  different knowledge.
- It might be the same information as another piece of code with totally different
  implementation.

For **example**: In a simple API client, one can be tempted to include some
constants used in the server part of the API, even from the database.  Yes, the
strings are the same, but the meaning is different: one talks about the
language used when communicating with the server, and the other tells you what
you will find in your database.

Perhaps you've implemented the one method time ago, with a different amount of
knowledge, thus it looks totally different from the one you're writing now and
you might not remember the old one.

## Don't repeat yourself - !code

Knowledge is not only code, you might find repeated knowledge:

- In superfluous documentation.
- In duplicated small libraries implemented in many teams inside the same big dev team.
- In how you **do** things like deployment, code versions, testing.
- In the communication with your team: endless meetings saying the same again and again anyone?

## Last responsible moment

The [last responsible moment][LRM] tells us to “delay commitment until the
moment at which failing to make a decision eliminates an important
alternative”.  (Mary and Tom [Poppendieck][popllc], Lean Software Development: An Agile
Toolkit).

Right now, do you have all the information you need to remove a duplication? If
you don't remove the duplication now, will something bad happen tomorrow?

For **example**: when you're developing a new subsystem in your application,
some code might start to appear as "it is doing the
same thing", you know you have another sprint and a half with this new
subsystem, so you can wait till the subsystem is finished to take a look and
refactor (red, green, next step refactor). Here you might have repeated
yourself 5 times, and still you know it is not time to refactor.

You might be just adding a feature to that subsystem after it has been
finished. You “do your thing” with surgical precision and you add your extra
bunch of tools to help you do accomplish your task. But, did you know that some
or all of these tools are in the subsystem? Perhaps they're small tools that
you've never stumbled upon, even if the internal API is well documented. In a
code review, or during a pair programming session, your coworker might point
you to them and you will use them. You might refactor them a bit to make them
more visible. Here a  **second** time was enough.

## The team issue.

When working in teams, that *second time* for you might be the 6th time for the
team. You might not even get a "second repetition" and do the same once per
team member. You could write down some guidelines to help team
members to find the knowledge they're looking for and avoid “invent
everything”, because they won't see the “third time” in order to refactor.

## Pareto principle.

The pareto principle states that 80% of the effects come from 20% of the
causes. In our case, we can achieve 80% of DRY with 20% of effort. Does the
other 20% of DRY deserve the rest of the effort? Again no golden rule :(. This
depends on the issue at hand, the project, the status of the project at the
very moment of taking the decision.

Many times the effort removing duplicated information is small, because we were
able to say that "if we don't do it now, tomorrow it will be late". You might
know that each sub-team in a big engineering team, have developed their own way
to deploy an application. They all do it almost in the same way with their
personal touch of spice. Can your engineering team tackle that issue now? 80/20
principle.

## Summary

Applying only one principle might not be a good idea. There is more to software
principles than meet the eye you can use in your advantage.

![transformers][transformers]


[justinweiss_post]: http://www.justinweiss.com/blog/2014/02/28/i-dry-ed-up-my-code-and-now-its-hard-to-work-with-what-happened/
[justinweiss_twitter]: https://twitter.com/justinweiss
[LRM]: http://blog.codinghorror.com/the-last-responsible-moment/
[pareto]: http://skillcrush.com/2012/08/24/pareto-principle/
[popllc]: http://www.poppendieck.com
[transformers]: more.than.meets.the.eye.jpg "More than meets the eye"

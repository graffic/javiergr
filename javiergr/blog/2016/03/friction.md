title: Friction in the real world
date: 2016-03-09
category: lean
published: true
summary: The force that resist motion in software development

Reading [this article](http://www.leanessays.com/2015/08/friction.html) by [Mary Poppendieck](http://www.poppendieck.com) about friction in the software industry made me look back to those times where things weren't going as smooth as one would like. That problem had a name: **friction**. Let me share with you some of those moments.

## Code producer-consumer

There's a team that produces code and other team that consumes that code. The exposed code surface becomes a friction area.

Two teams working with different goals solve problems in a different way. One team is assigned the task of creating an API or *core* libraries. Their focus is to keep those libraries clean, extendable, with many features and while doing something new (because if not they could have used existing libraries).

On the other side, the team using that code to solve business problems not only they don't need all those fancy features but they have a difficult time adapting the idealized utilities to the real world. They're not allowed to change them(another team is doing it) plus they have very few knowledge if they wanted to.

Both teams get angry/pissed off at each other:

- **Team A**: they don't appreciate our work and the care we've put on that. They don't put time to understand the mechanics, they're lazy.
- **Team B**: they don't know what are we dealing with. Why do we have to deal with their toy and not solve it by ourselves.

Have you tried to make those teams *full-stack* by having them eating their own dog food?  Having your teams being able to write and decide about the tools they use to solve the business need at hand so they are fully empowered.

People working in a code base know about the problems it has (be it new or legacy). Give them the space to scratch that itch and you will get a great motivated *scratch*.

At the same times this enables incremental improvements by scratching one itch here and there, instead of waiting for the new library or the new engine to come out to understand that it doesn't solve the problem.

## Shared artifacts

In every system there are parts that are common or reused by others. These libraries, APIs or even other system expose a shared area that is usually a source of friction.

### Shared database

One of the biggest issues I've seen is a shared database system. It becomes the center of the world because every system wants to store their data there: It is just an ip and a password.

Each system has its own needs. That's the first hint to start looking at what the business requires and not at what we have right now installed. Although in the end an entire database is shared because it we want only one source of authority for many things.

If your business sell cars, the data related to a car is different depending on who is using that data: the factory, the show room, the sales person. Imagine the development units fighting on how to shape the car entity for each one. Plus the synchronization needed to release those changes in the data to all the involved systems.

If each system uses their own data storage (even if it is the same technology) and decides about the data they store, the friction is reduced. And for data that is stored in other system they just need to know which system is the source of authority of that data.

So a car might share the frame number in all the storages being the factory system the one that is the source of authority.

Also if each system to decide what technology they need they can find something that serves better their needs: SQL, key-value, etc.

### Shared core system

A big bunch of code becomes the center of the system's universe. Every benefit and problem is related to that piece of code.

Perhaps it was created by those *code producers* or it evolved from the early stages of a system and now it is being used in every other system because "it's the way". It defines almost every application and it's one size that should fit everybody.

Not many people are allowed to change the shared core, have the knowledge to change it or want to take the risk to change it.

As before, the needs for one system shouldn't impose restrictions in the next one. Some parts might be equal. Just those very specific parts that usually have clear goals.

It is very different to share a serialization protocol library than an entire REST API system with included database. Picking just the needed parts helps reducing the friction area.

Those small parts are also easy to develop and improve by many teams because their scope is so small that everybody can understand and there is not much space for different needs or over-engineering. As you could easily create another library for other needs or build on that small piece.

## The new version

Replacing a big system by the new faster, modern big system that will solve almost all the problems the old system has.

Mary did a good research pointing out the new digital policies in UK and USA based on Estonia experiences. Small teams dealing directly with the users. Creating many small applications or growing a small one step by step.

In the same way the UK failed to replace their old UK National Health system. Your next new version of the old system will fail. But this doesn't mean that you have to keep your old systems as they are.

Delivering software in small increments and slowly taking over the old application can help. But don't forget to remove intermediaries in the process or you might end up having a new version that is not what is needed.

## Closing

For me friction has become an important point to take into account into a decision. Besides good or bad based on what each one involved would think is better. How much friction does it create? and who will suffer it?

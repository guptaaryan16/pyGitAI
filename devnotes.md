Developer Notes
===============

The project is a plug-n-play interface for LLM models in git based projects. This allows a lot more 
use of LLMs in everyday development and thus increasing the productivity of the developers in the 
process. I know the LLMs are not even close to producing the well-thought software code as need by 
enterprises, but they come in handy in reducing day-to-day repetitive development tasks. Let's see 
how well this project grows and help in reducing the boilerplate tasks that provide friction in
writing and maintaining packages in vast software ecosystems.


Project Methodology
-------------------

The project follows a "Developer first" approach with the maximum effort towards the effective integration of industry standard tools like graphite and LLMs that come in the market. My focus is also to make sure you have a positive  developer experience using this tool on your local projects and this doesn't hamper your ability to work on your git projects in any way. The project keeps in mind the needs of OSS developers and commandline based developers who love to code just using their keyboard and want to maintain the privacy of their codebases ( local LLM support can be expected in future ) . 

The use of tools like GitPython which were developed as hobby projects like this have provided me a great motivation to follow all standard practices in Python for the development of this project. The idea is not reinventing the wheel but to make it more usable wherever possible. Another question that may come in your mind is, Yes, I saw the project `AICommits` and did not like the use of NodeJS env which makes the project less maintainable(for instance incorportating model weights direclty) and in general leads to fewer choices available to the developers in the future. So this is my alternative, which you may or may not like, but again in general both is fine by me.

Also as a remark, I believe Python envs are usually more suitable for CLI applications especially those that uses LLMs as the developer experience of Python scripting is easier for most developers to adapt to and is thus better than JS. Don't Bash my opinion by creating any spam issues, this is just my take on things as they are.

If you would like to contribute or support the development of the project, please reach out to `guptaaryan16@gmail.com`.

Scope of the Project in Future
-------------------------------

I have no idea where the OSS community is going to take this project. Right now, my main focus is to remove all the bugs as fast as possible and make the developer experience using this tool worthwhile. I know you may expect me to keep track of everything that happens in the project and support the new projects related to AI that comes in the market, frankly speaking its impossible to cover and support everything on my own. So what I want is people to come up and help me as much as possible.

As for my personal ambitions for the project, I hope that I become a better programmer and communicator as the project progresses in the future. Also may the project help as many developers as possible.


New Ideas Planned for future ( May be subject to discussion for the community )
--------------------------------------------------------------------------------
1. To-Do app (May be a Notion integration) for what to be implemented with the branches
2. Try to shift the codebase towards low level languages like Rust or C++ (to make it fast :-|)
3. The API should support making Plugins for the VS code and other git based CLI tools like ghstack 
   and Graphite
4. Work on better documentation and features as requested by users.
5. Completing some work on local model inference and adding training options for
   LLM models to be trained on 
6. The long term aim is to make small changes happen directly by the developers and 
   have tools like better and more open sourced than copilot CLI to understand and improve the developer workflows. 


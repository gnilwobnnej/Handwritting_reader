# Handwritting_reader

This program uses [Ollama](https://ollama.com/) <img src="https://ollama.com/public/ollama.png" alt="ollama" height="75"> utilizing LLaVa to read text from an image and Gemma3 to summerize or rewrite the text that it finds. 

It doesn't seem to like my handwritting, but it likes my roommates handwritting. 

- [x] make the program 
- [ ] write a better readme
- [ ] figure out a way for it to keep the formatting of the text document
- [x] edit the code for it to give better prompts. 
- [x] maybe add user inserted prompts
- [ ] test other handwritting with the model.

One should not code on very little sleep.

update: 5/12/2025

Changed the model that reads the text from the image to gemma3.

Also changed it so that the user can imput their own questions. They can have gemma3 answer all the questions to their heart desires. When they are done the user will type quit and the conversation and the text will be saved to the text file that they named earlier. or left blank and it will timestamp it.

I kept the other version of what I was having gemma do if it's needed, just commented out.

testfinel.txt = is my test with the new setup on 2.jpg

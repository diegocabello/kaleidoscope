# KALEIDOSCOPE README

## About

The objective of this project is to make an application of the most important technology this century, AI, through the invention of a new digital medium, the **V-BOOK**. The **V-BOOK** is an animated video slideshow of AI-generated images corresponding to segments of text from a book, with potential to expand into stories explicitly written in that medium. This application was chosen with intent to preserve literacy and literary culture.

## How it works

The creation of a **V-BOOK** involves three main steps: parsing and annotating a book, passing the text and annotations through image-generation and text-to-speech APIs, and splicing together animated videoclips. The code for this is entirely written in Python.

1. Text Parsing and Annotations
   - A **book** is put into a text file.
     - The books are sourced from [Project Gutenberg](https://gutenberg.org), a libary of public-domain books.
     - Examples of books to be used initially are:
       - Pride and Prejudice
       - Alice in Wonderland
       - The Memoirs of Casanova
   - The book is **parsed**
     - Split into sentences, each sentence is tagged as either a quote or a paragraph
     - Longer corresponding sentences are split further, shorter ones are concatenated, into "bits" that will be fed into the image-generators as prompts
     - Each "bit" then loaded into an Excel file and denoted as seperate quote or paragraph by alternating colored and shaded bands
   - The parsed text is manually **annotated** in Excel with categories such as setting descriptions, shot type, speaker, charachter descriptions, and framing
   - The annotations are **formatted** into prompts
2. Image, Audio, and Caption Generation
   - The formatted prompts are passed through an **AI-image generator**, most likely to be Midjourney, and saved locally
     - Using FFmpeg, The images are zoomed in on, blurred, and darkened for the video background
   - The text bits are passed through a **text-to-speech** API (still looking for the right candidate)
   - The text bits are also centered in an image for **captions**
   - All of this is done asyncronously for each "bit" along with video generation
3. Video Generation
   - The image is **pasted on top** of the corresponding background image, and increases in size in a series of frames according to a sqrt equasion (may have to change it), over the duration of the video, which is determined by the length of the audio
   - Captions are pasted at the bottom
   - The **videoclip** is saved locally
   - Done asyncronously for each "bit" along with Image, Audio, and Caption generation
   - The clips are then **stitched** together into the final product

## Project Status

At the inital time of commit, on 26 Jan 2024, there is still a lot to be done until release. This is currently the product of about 20 days of solo coding. Some features that still need to be added are, centering the captions vertically, formatting the prompts, testing the prompts in various engines, finding a text-to-speech API, changing the zoom equasion, and adding the asyncronous functionality. Additional features to be added include automatically detecting which charachter is speaking and automatically determine whether framing should be the speaker or the subject being spoken about when the "bit" is a quote. Then all the promotional materials, marketing plans, and monetization strategies need to be finalized, but that is another area outside the scope of GitHub. The codebase also needs to be cleaned up and annotated well, and python packages need to be managed.

This was uploaded as an archive but if anyone from the few people I share this to want to contribute, I will gladly accept help and will be willing to share some of the profits.

Created by Diego Cabello

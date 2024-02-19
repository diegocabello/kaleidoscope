# KALEIDOSCOPE README

## About

The objective of this project is to create an application of the most important technology from this generation, AI, in a new digital medium: the **V-BOOK**. A **V-BOOK** is an animated and narrated slideshow of AI-generated images derived from a book. This medium was written with expansion in mind, including contracting with publishers and screenplay writers for drafting, and expanding into stories explicitly written for that medium. This application was chosen specifically with intent to preserve literacy and literary culture.

## How it works

The creation of a **V-BOOK** involves three main steps: parsing and annotating a book, passing the text and annotations through image-generation and text-to-speech APIs, and creating and splicing together animated videoclips. The main language for this project is Python.

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
     - Each "bit" then loaded into an Excel file and denoted as seperate bit and seperate quote or paragraph by alternating colored and shaded bands
   - The parsed text is manually **annotated** in Excel with categories such as setting descriptions, shot type, speaker, charachter descriptions, and framing
   - The annotations are **formatted** into prompts
2. Image, Audio, and Caption Generation
   - The formatted prompts are passed through an **AI-image generator**, most likely to be Midjourney, and saved locally
     - Using FFmpeg and PIL, The images are zoomed in on, blurred, and darkened for the video background
   - The text bits are passed through a **text-to-speech** API (still looking for the right candidate)
   - The text bits are also centered in an image for **captions**
   - All of this is done asyncronously for each "bit" along with video generation
3. Video Generation
   - The image is **pasted on top** of the corresponding background image, and increases in size in a series of frames according to a sqrt equasion (presently) over the duration of the video, which is determined by the length of the audio
   - Captions are pasted at the bottom
   - The **videoclip** is saved locally
   - Done asyncronously for each "bit" along with Image, Audio, and Caption generation
   - The clips are then **stitched** together into the final product

## Project Status

This project is mostly complete and is presentable, but there is a little more code to be done including: adding asyncronous functionality, managing python packages, and making style, characters, and settings more consistent. This project is currently in the planning phase for marketing, financing, and deployement. 

Created by Diego Cabello

# 12433693_text-recognition-german

## Overview
The goal of this project is to build and fine-tune an existing Optical Character Recognition (OCR) model to recognize both English and German printed text. The base model used will be pretrained architecture (TrOCR) that will be adapted to handle German-soecific secial characters such as **ä, ö, ü, and ß**. Finally, the project's goal is to translate these german words to english through a Docker-contained application.

## Motivation
As an international student constantly trying to improve their German language skills, it is really important to have a tool that simply recognizes a picture of a word and translates it. Of course, ChatGPT does it already, but it also requires a really good data connection, and my goal is to create a model that works without the internet. 

## Project Type: **Bring your own method**
The project will re-use the existing TrOCR neural network and be fine-tuned to improve its capability in recognizing texts that include German characters. This improvement will be achieved through a combination of an existing English dataset and synthetically generated German word images. To improve final results, a few modifications will be done, such as augmentation tweaks to the train dataset and vocabulary extension to include special characters.

## Dataset
- **Primary Dataset**: A collection of English word images stored as JPG files, with their labels stored in XML format (~1100 words).
- **Test Dataset**: A separate set of English word images in the same format as the primary dataset (~1100 words). This will be split into validation and test.
- **Additional Synthetic Data**: Automatically generated German word images, including special characters like 'ä, ö, ü, ß' (~5000 words). This list is currently in JSON format. 

## Work Breakdown Structure

| Task | Description | Time Estimate |
| -----|-------------|---------------|
| Dataset Preparation | Parse XML to CSV and Generate synthetic German data | 
| Model Setup | Load and test baseline TrOCR separately on English dataset and a combination of English and German dataset |
| Training and Fine-Tuning | Fine-tune model with German dataset |
| Evaluation| Evaluate on English-German test dataset and compare with baseline results |
| Improvements | Check if results can be improved through augmentation twears and vocabulary extension. Evaluate again |
| Building Application | Build a demo Docker app to make a useable application. Add translation/spell-check |
| Final Report and Presentation | Write final report and create presentation |


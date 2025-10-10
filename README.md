# 12433693_text-recognition-german

## Overview
**Topic: Text Recognition**

The goal of this project is to build and fine-tune an existing Optical Character Recognition (OCR) model capable of recognizing both English and German printed text. The base model used will be the pretrained **TrOCR** architecture, which will be adapted to handle German-specific special characters such as **ä, ö, ü, and ß**. Finally, the project aims to translate these German words into English through an application packaged inside a Docker container.

## Motivation
As an international student, continually improving my German language skills, having a lightweight, offline tool that can recognise a picture of a word and translate it into English would be extremely helpful. Although existing tools (like ChatGPT) can already perform this task better, they require an active internet connection. My goal is to create a model that can perform optical recognition and translation without needing the internet.

## Project Type: **Bring your own method**
The project reuses the existing TrOCR neural network and fine-tunes it to improve its capability in recognising texts that include German characters. This improvement will be achieved using a combination of an existing English OCR dataset and a synthetically generated German dataset. To improve final results, a few modifications will be done, such as augmentation tweaks to the train dataset and vocabulary extension to include special characters. To further enhance results, several modifications will be applies, such as:
- Augmentation tweaks: to improve results through distortions.
- Vocabulary extension: to include German-specific characters.

## Dataset
- **Primary Dataset**: The **[IIIT-5K Word Dataset](https://www.kaggle.com/datasets/prathmeshzade/iiit5k-words) (Mishra et al., BMVC 2012)**, containing ~2,000 training and ~3,000 testing cropped word images from real-world scenes. Each image is annotated with a ground-truth word label. This dataset is widely used for OCR benchmarking.
- **Additional Synthetic Data**: Automatically generated German word images, including special characters like 'ä, ö, ü, ß' (~5000 words). This list is currently in JSON format and will be synthetically converted into images for fine-tuning the model.
- **Test Split**: The official IIIT-5K test set will be used for English evaluation, and a small portion of the synthetic German dataset will be reserved for multilingual testing.

## Work Breakdown Structure

| Task | Description | Time Estimate |
| -----|-------------|---------------|
| Dataset Preparation | Work with IIIT-5K files, verify image paths, and generate synthetic German data | 12 hours |
| Model Setup | Load and test the baseline TrOCR separately on the English dataset, and then test with a combination of English and German datasets | 8 hours |
| Training and Fine-Tuning | Fine-tune the model with English-German dataset | 20 hours |
| Evaluation| Evaluate performance on English-German test dataset and compare with baseline results | 10 hours |
| Improvements | Experiment with data augmentation and vocabulary extensions, retrain and re-evaluate | 15 hours |
| Application Development | Build a simple Docker-based demo app with translation and optional spell-checking | 10 hours |
| Final Report and Presentation | Write final report and create presentation | 8 hours |

## References
https://ojs.aaai.org/index.php/AAAI/article/view/26538
https://cs.stanford.edu/~acoates/papers/coatesetal_icdar_2011.pdf



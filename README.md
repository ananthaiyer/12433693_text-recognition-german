# 12433693_text-recognition-german

## Overview
**Topic: Text Recognition**

The goal of this project is to build and fine-tune an existing Optical Character Recognition (OCR) model capable of recognizing both English and German printed text. The base model used will be the pretrained **TrOCR** architecture, which will be adapted to handle German-specific special characters such as **ä, ö, ü, and ß**. The project focuses on improving OCR performance for German text while maintaining reasonable performance on English text. All experiments, including data preparation, baseline evaluation, and fine-tuning, are implemented as part of a reproducible software pipeline.

## Motivation
As an international student who is continually improving my German language skills, having a lightweight, offline tool that can recognise a picture of a word and translate it into English would be extremely helpful. Although existing tools (like ChatGPT) can perform this task better, they require an active internet connection. My goal is to create a model that can perform optical recognition and translation without needing the internet.

## Project Type: **Bring your own method**
The project reuses the existing TrOCR neural network and fine-tunes it to improve its capability in recognising texts that include German characters. This improvement will be achieved using a combination of an existing English OCR dataset and a synthetically generated German dataset. 

Several techniques are explored to improve performance:
- Data augmentation to increase robustness
- Mixed English–German training to avoid catastrophic forgetting
- Hyperparameter tuning and training stabilisation techniques

## Dataset
- **Primary Dataset**: The **[ICDAR 2003 Robust Reading Competition dataset](http://www.iapr-tc11.org/mediawiki/index.php?title=ICDAR_2003_Robust_Reading_Competitions)**, containing ~1150 training and ~330 testing cropped word images from real-world scenes. Each image is annotated with a ground-truth word label. This dataset is widely used for OCR benchmarking. 
- **Additional Synthetic Data**: Automatically generated German word images (**[source](https://github.com/Jonny-exe/German-Words-Library/blob/master/German-words-5000-words.json)**), including special characters like 'ä, ö, ü, ß' (~5000 words). This list is currently in JSON format and will be synthetically converted into images for fine-tuning the model.
- **Test Split**: The official ICDAR test set will be used for English evaluation, and a small portion of the synthetic German dataset will be reserved for multilingual testing.

**Note**: While preparing the English test dataset, some files could not be used due to corruption issues in the original archive. These files were removed after extraction so that the dataset could be processed correctly by the preprocessing pipeline.
Since the dataset is derived from a third-party source, it is not included directly in the GitHub repository or uploaded via GitHub Releases. Instead, the prepared version of the dataset is provided separately as a ZIP archive through my personal Google Drive. To reproduce the experiments, please download the archive from the link below and place it in the `Datasets/` directory.

(Download link: [Google Drive](https://drive.google.com/drive/folders/1F4oF5h3M77UW568W_Z_TNGwsasvl9-pK?usp=sharing))


## Evaluation Metrics

Model performance is evaluated using standard OCR metrics:
- **Character Error Rate (CER)**
- **Word Error Rate (WER)**

These metrics are used consistently across baseline and fine-tuned models to allow fair comparison.

## Target Performance

The initial target was to:
- Establish a working English baseline using the pretrained TrOCR model.
- Reduce the German CER and WER compared to the baseline model by fine-tuning on synthetic German data.
- Maintain comparable English performance while improving German recognition.

## Results
The pretrained TrOCR model performs reasonably well on English text but struggles significantly with German-specific characters.

After fine-tuning on a mixed English–German dataset with additional regularization and data augmentation, the final model shows:
- Improved CER and WER on German test data compared to the baseline.
- Stable or slightly improved performance on English test data.


## Quantitative Results

The table below summarizes the OCR performance for baseline, intermediate fine-tuning, and final fine-tuning models on both English and German datasets. Performance is measured using Character Error Rate (CER) and Word Error Rate (WER).

| Model Version | Language | #Samples | CER | WER | Word Accuracy |
|--------------|----------|----------|-------|-------|-----------------|
| Baseline (TrOCR) | English | 331 | 0.542 | 0.607 | 0.393 |
| Baseline (TrOCR) | German | 300 | 0.952 | 1.000 | 0.000 |
| Moderate Fine-tune | English | 331 | 0.492 | 0.680 | 0.320 |
| Moderate Fine-tune | German | 300 | 0.495 | 0.993 | 0.007 |
| **Final Fine-tune** | **English** | **331** | **0.297** | **0.535** | **0.465** |
| **Final Fine-tune** | **German** | **300** | **0.394** | **0.993** | **0.007** |

Overall, the pretrained TrOCR baseline performs reasonably on English text but fails almost completely on German text due to vocabulary mismatch. Fine-tuning substantially reduces the Character Error Rate for both languages. The final fine-tuned model achieves the best overall performance, particularly for English, while also significantly improving German character recognition compared to the baseline.
However, note that the German WER remains high even after fine-tuning. This is mainly due to frequent character-level errors in longer words, where a small number of character mistakes can cause an entire word to be counted as incorrect.


## Time Spent
The following table shows the **actual approximate time spent** on each task. The reported time is for documentation purposes only and does not affect grading.

| Task | Time Spent |
|-----|------------|
| Dataset Preparation | ~4 hours |
| Model Setup & Baseline Experiments | ~5 hours |
| Training & Fine-Tuning | ~25 hours |
| Evaluation & Error Analysis | ~3 hours |
| Model Improvements & Experiments | ~15 hours |
| Documentation & Reporting | ~2 hours |


## How to Run

### Requirements
- **Python version:** 3.11 (kernel: 3.11.13)  
- Required libraries are listed in `requirements.txt`.

To install dependencies:
```bash
pip install -r requirements.txt 
```

### Running Experiments

The project is primarily notebook-based. Each notebook corresponds to a specific stage of the OCR pipeline and can be executed independently in order.

- **`1_Data_Preparation.ipynb`**  
  Prepares the datasets used throughout the project. This includes parsing the ICDAR annotations, verifying image paths, and loading the German word list used for synthetic data generation.

- **`2_Baseline_English.ipynb`**  
  Evaluates the pretrained TrOCR model on the English ICDAR test set without any fine-tuning. This notebook establishes the English baseline performance using CER and WER.

- **`3_Baseline_German.ipynb`**  
  Evaluates the same pretrained TrOCR model on German word images. This baseline highlights the performance degradation caused by language and vocabulary mismatch and motivates fine-tuning. Synthetic images are created in this notebook.

- **`4_Finetune.ipynb`**  
  Contains the initial fine-tuning experiments using a combined English–German dataset. This notebook explores basic hyperparameter choices and training behaviour.

- **`5_Finetune_latest.ipynb`**  
  Implements the final and improved fine-tuning configuration, including data augmentation, learning-rate warmup, gradient accumulation, and stronger regularization. Final evaluation on both English and German test sets is performed in this notebook.


**Note**: This code includes a model checkpoint to save the best model generated during fine-tuning. This is not included in the file.

### Testing

Basic unit tests are provided using **pytest** to verify preprocessing and post-processing steps. To run tests in the root directory:
```bash
pytest
```
All tests pass successfully.

## Conclusion
This project demonstrates that a pretrained OCR model can be successfully adapted to German text using limited additional data and targeted fine-tuning. Synthetic data generation, careful training configuration, and evaluation using appropriate metrics were key to improving performance. However, the amount of synthetic data is relatively low, and increasing the number of generated images could further improve performance.

Run application: docker run --rm -p 8501:8501 german-ocr-demo 

## References

1. Coates, A., Carpenter, B., Case, C., Satheesh, S., Suresh, B., Wang, T., Wu, D. J., & Ng, A. Y. (2011).  
   *Text Detection and Character Recognition in Scene Images with Unsupervised Feature Learning.*  
   Computer Science Department, Stanford University.  
   [PDF link (Stanford)](https://cs.stanford.edu/~acoates/papers/coatesetal_icdar_2011.pdf)

2. Li, M., Lv, T., Chen, J., Cui, L., Lu, Y., Florencio, D., Zhang, C., Li, Z., & Wei, F. (2021).  
   *TrOCR: Transformer-based Optical Character Recognition with Pre-trained Models.*  
   Microsoft Research & Beihang University.  
   arXiv: [PDF link](https://ojs.aaai.org/index.php/AAAI/article/view/26538)



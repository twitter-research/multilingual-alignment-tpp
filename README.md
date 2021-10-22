# [Improved Multilingual Language Model Pretraining for Social Media Text via Translation Pair Prediction](https://arxiv.org/abs/2110.10318)

[![Open All Collab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/twitter-research/multilingual-alignment-tpp) [![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/twitter-research/multilingual-alignment-tpp/HEAD)

![image](multilingual_tpp.png)

Code for reproducing the paper **[Improved Multilingual Language Model Pretraining for Social Media Text via Translation Pair Prediction](https://arxiv.org/abs/2110.10318)** to appear at [The 7th Workshop on Noisy User-generated Text (W-NUT)](http://noisy-text.github.io/2021/) organized at EMNLP 2021. 

## Abstract

> We evaluate a simple approach to improving zero-shot multilingual transfer of mBERT on social media corpus by adding a pretraining task called translation pair prediction (TPP), which predicts whether a pair of cross-lingual texts are a valid translation. Our approach assumes access to translations (exact or approximate) between source-target language pairs, where we fine-tune a model on source language task data and evaluate the model in the target language. In particular, we focus on language pairs where transfer learning is difficult for mBERT: those where source and target languages are different in script, vocabulary, and linguistic typology. We show improvements from TPP pretraining over mBERT alone in zero-shot transfer from English to Hindi, Arabic, and Japanese on two social media tasks: NER (a 37% average relative improvement in F1 across target languages) and sentiment classification (12% relative improvement in F1) on social media text, while also benchmarking on a non-social media task of Universal Dependency POS tagging (6.7% relative improvement in accuracy). Our results are promising given the lack of social media bitext corpus.

## Citation
 
 Please cite as:
 
 > Mishra, S., & Haghighi, A. (2021). Improved Multilingual Language Model Pretraining for Social Media Text via Translation Pair Prediction. Proceedings of the 7th Workshop on Noisy User-generated Text (W-NUT 2021). [arXiv](https://arxiv.org/abs/2110.10318)
 
 
 ```bibtex
@inproceedings{mishra2021tpp,
  title={Improved Multilingual Language Model Pretraining for Social Media Text via Translation Pair Prediction},
  author={Mishra, Shubhanshu and Haghighi, Aria},
  booktitle={Proceedings of the 7th Workshop on Noisy User-generated Text (W-NUT 2021)},
  year={2021},
  address={Online},
  publisher={Association for Computational Linguistics},
  pages={1--8},
  eprint={2110.10318},
  archivePrefix={arXiv},
  primaryClass={cs.CL}
}
 ```


## Reproducibility

Following steps allow reproducing experiments in the paper:

1. Run mBERT finetuning
2. Fine-tune on specific task (NER, POS, Sentiment).

Both steps can be run via files in `./notebooks/`. 

More details in the paper.

## Datasets

We provide example formats of the datasets in the `/data` folder. The NER data for English, Arabic, and Japanese is internal. 
Details for processing data can be found in `./src` folder. 


## Security Issues?

Please report sensitive security issues via Twitter's bug-bounty program (https://hackerone.com/twitter) rather than GitHub.


# Comparing Writing Style Across Reuters Regions

Short project to extract, clean and analyze writing style differences between Reuters articles by region (US vs Europe). The analysis pipeline extracts articles, computes linguistic features (POS, NER, sentiment, embeddings), runs topic modeling and classification, and outputs CSVs and per-article text files.

## Key files
- [extract_reuters.py](extract_reuters.py) — SGM parsing utilities (see functions [`get_first`](extract_reuters.py) and [`parse_reuters_sgm`](extract_reuters.py)).
- [reuters_analysis.ipynb](reuters_analysis.ipynb) — Main analysis notebook (contains functions like [`compute_style_features`](reuters_analysis.ipynb) and [`pos_features`](reuters_analysis.ipynb)).
- Input data: [input/reuters_regions.csv](input/reuters_regions.csv)
- Extracted article text: saved under `articles/` (e.g. [articles/us/article_1041.txt](articles/us/article_1041.txt))
- Processed outputs (examples):
  - [output/prem_features.csv](output/prem_features.csv)
  - [output/pos_topic_features.csv](output/pos_topic_features.csv)
  - [output/pos_topic_ner_features.csv](output/pos_topic_ner_features.csv)
  - [output/pos_topic_ner_sentiment_features.csv](output/pos_topic_ner_sentiment_features.csv)
  - [output/pos_topic_ner_sentiment_embedding_features.csv](output/pos_topic_ner_sentiment_embedding_features.csv)
  - [output/reuters_articles.csv](output/reuters_articles.csv)

## Quickstart

1. Create a Python environment and install dependencies (example):
```sh
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
# If no requirements.txt, at minimum:
pip install pandas numpy scikit-learn seaborn matplotlib spacy textblob sentence-transformers umap-learn
python -m spacy download en_core_web_sm
```

2. Extract articles from raw SGM files:
```sh
python extract_reuters.py
```
This uses [`parse_reuters_sgm`](extract_reuters.py) and writes `output/reuters_regions.csv`.

3. Open and run the analysis:
- Launch Jupyter and run the notebook: [reuters_analysis.ipynb](reuters_analysis.ipynb)
```sh
jupyter lab
# open reuters_analysis.ipynb and run cells
```
The notebook:
- reads `input/reuters_regions.csv` and generated CSVs,
- computes style features via [`compute_style_features`](reuters_analysis.ipynb),
- performs topic modeling, POS/NER, sentiment (TextBlob), embeddings (Sentence-BERT),
- saves feature CSVs into `output/`.

4. Reproducible outputs are written to `output/` (CSV files and embedding files). Example: [output/prem_features.csv](output/prem_features.csv).

## Notes & tips
- The notebook contains cells to balance datasets, build classifiers (logistic regression, RF, SVM), compute feature importance and visualize embeddings (PCA, t-SNE, UMAP).
- If embedding model downloads fail, run the sentence-transformers installation step manually before executing embedding cells.
- Large embeddings and model inference may require significant memory. Consider running embedding steps on a machine with enough RAM or batch the encoding.

## Project structure (important paths)
- extract script: [extract_reuters.py](extract_reuters.py)
- main notebook: [reuters_analysis.ipynb](reuters_analysis.ipynb)
- raw input: [input/reuters_regions.csv](input/reuters_regions.csv)
- processed CSV outputs: `output/` (see examples above)
- article text outputs: `articles/us/` and `articles/europe/`

## Reuse & extension
- Swap topic model settings in the notebook (LDA parameters, vectorizer).
- Add other language models for richer embeddings or replace TextBlob sentiment with transformer-based sentiment analyzers.
- Use `output/features_with_topics.csv` as the consolidated feature table for ML experiments.

## License
Choose an appropriate license for your work (e.g., MIT). Add `LICENSE` file if needed.

```// filepath: README.md

# Comparing Writing Style Across Reuters Regions

Short project to extract, clean and analyze writing style differences between Reuters articles by region (US vs Europe). The analysis pipeline extracts articles, computes linguistic features (POS, NER, sentiment, embeddings), runs topic modeling and classification, and outputs CSVs and per-article text files.

## Key files
- [extract_reuters.py](extract_reuters.py) — SGM parsing utilities (see functions [`get_first`](extract_reuters.py) and [`parse_reuters_sgm`](extract_reuters.py)).
- [reuters_analysis.ipynb](reuters_analysis.ipynb) — Main analysis notebook (contains functions like [`compute_style_features`](reuters_analysis.ipynb) and [`pos_features`](reuters_analysis.ipynb)).
- Input data: [input/reuters_regions.csv](input/reuters_regions.csv)
- Extracted article text: saved under `articles/` (e.g. [articles/us/article_1041.txt](articles/us/article_1041.txt))
- Processed outputs (examples):
  - [output/prem_features.csv](output/prem_features.csv)
  - [output/pos_topic_features.csv](output/pos_topic_features.csv)
  - [output/pos_topic_ner_features.csv](output/pos_topic_ner_features.csv)
  - [output/pos_topic_ner_sentiment_features.csv](output/pos_topic_ner_sentiment_features.csv)
  - [output/pos_topic_ner_sentiment_embedding_features.csv](output/pos_topic_ner_sentiment_embedding_features.csv)
  - [output/reuters_articles.csv](output/reuters_articles.csv)

## Quickstart

1. Create a Python environment and install dependencies (example):
```sh
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
# If no requirements.txt, at minimum:
pip install pandas numpy scikit-learn seaborn matplotlib spacy textblob sentence-transformers umap-learn
python -m spacy download en_core_web_sm
```

2. Extract articles from raw SGM files:
```sh
python extract_reuters.py
```
This uses [`parse_reuters_sgm`](extract_reuters.py) and writes `output/reuters_regions.csv`.

3. Open and run the analysis:
- Launch Jupyter and run the notebook: [reuters_analysis.ipynb](reuters_analysis.ipynb)
```sh
jupyter lab
# open reuters_analysis.ipynb and run cells
```
The notebook:
- reads `input/reuters_regions.csv` and generated CSVs,
- computes style features via [`compute_style_features`](reuters_analysis.ipynb),
- performs topic modeling, POS/NER, sentiment (TextBlob), embeddings (Sentence-BERT),
- saves feature CSVs into `output/`.

4. Reproducible outputs are written to `output/` (CSV files and embedding files). Example: [output/prem_features.csv](output/prem_features.csv).

## Notes & tips
- The notebook contains cells to balance datasets, build classifiers (logistic regression, RF, SVM), compute feature importance and visualize embeddings (PCA, t-SNE, UMAP).
- If embedding model downloads fail, run the sentence-transformers installation step manually before executing embedding cells.
- Large embeddings and model inference may require significant memory. Consider running embedding steps on a machine with enough RAM or batch the encoding.

## Project structure (important paths)
- extract script: [extract_reuters.py](extract_reuters.py)
- main notebook: [reuters_analysis.ipynb](reuters_analysis.ipynb)
- raw input: [input/reuters_regions.csv](input/reuters_regions.csv)
- processed CSV outputs: `output/` (see examples above)
- article text outputs: `articles/us/` and `articles/europe/`

## Reuse & extension
- Swap topic model settings in the notebook (LDA parameters, vectorizer).
- Add other language models for richer embeddings or replace TextBlob sentiment with transformer-based sentiment analyzers.
- Use `output/features_with_topics.csv` as the consolidated feature table for ML experiments.

## License
Choose an appropriate license for your work (e.g., MIT). Add `LICENSE` file if needed.

# hackathon_idfm_octo_2024
Hackathon IDFM 2024 - Equipe 6


## To setup environment

```shell
virtualenv .venv
source .venv/bin/activate
echo "../../../../" >> ./.venv/lib/$(ls ./.venv/lib/)/site-packages/local_path.pth
pip install -r requirements.txt
```

## To run the app

```shell
streamlit run ./sources/streamlit.py
```

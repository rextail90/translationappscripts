import pandas as pd

INPUT = "results/translation_scored.csv"
OUTPUT = "results/translation_scored.html"

def main():
    df = pd.read_csv(INPUT)
    df.to_html(OUTPUT, index=False, classes="table table-striped")

    print(f"Created HTML table at: {OUTPUT}")

if __name__ == "__main__":
    main()


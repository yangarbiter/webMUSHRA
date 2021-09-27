import pandas as pd


def main():
    df = pd.read_csv("./results/subjective_evalaution/lss.csv")

    competitors = ["original", "torchaudio", "tacotron2waveglow", "nvidia"]

    def get_competitor_name(name):
        for comp in competitors:
            if f"_{comp}_" in name:
                return comp

    df['competitor'] = df['trial_id'].apply(get_competitor_name)

    print(df.groupby(["competitor"]).mean())
    print(df.groupby(["competitor"]).sem())

    import ipdb; ipdb.set_trace



if __name__ == "__main__":
    main()

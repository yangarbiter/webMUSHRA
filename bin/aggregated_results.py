import pandas as pd

ignore_names = [
    "A23KAJRDVCVGOE",
    "A1N3YG2X9SO4PN",
]

def main():
    #df = pd.read_csv("./results/subjective_evalaution/lss.csv.bak")
    df = pd.read_csv("./results/subjective_evalaution/lss.csv")

    #competitors = ["original", "torchaudio", "tacotron2waveglow", "nvidia2"]
    competitors = ["original", "vocoder_waveglow", "vocoder_wavernn_nvidia",
                   "vocoder_wavernn_fatchord", "vocoder_fatchord"]

    def get_competitor_name(name):
        for comp in competitors:
            if f"_{comp}_" in name:
                return comp

    df['competitor'] = df['trial_id'].apply(get_competitor_name)
    df = df.drop(df[df['name'].apply(lambda x: x in ignore_names)].index)
    df['rating'] = df['stimuli_rating'].apply(lambda x: int(x))

    print(df.groupby(["competitor"]).mean())
    print(df.groupby(["competitor"]).sem())

    import ipdb; ipdb.set_trace



if __name__ == "__main__":
    main()

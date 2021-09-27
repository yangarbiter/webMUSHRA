#!/bin/bash

cp ../torchaudio-benchmark/tts-subjective/audio_samples/original/* configs/resources/samples/method_a/
cp ../torchaudio-benchmark/tts-subjective/audio_samples/nvidia/* configs/resources/samples/method_a/
cp ../torchaudio-benchmark/tts-subjective/audio_samples/torchaudio/* configs/resources/samples/method_a/
cp ../torchaudio-benchmark/tts-subjective/audio_samples/tacotron2waveglow/* configs/resources/samples/method_a/

./bin/convert_mono_to_stereo.sh \
    ./configs/resources/samples \
    ./configs/resources/samples_stereo

./bin/divide_audio_dir.py \
    --seed 777 \
    --num_wavs_in_each_subset 25 \
    ./configs/resources/samples_stereo \
    ./configs/resources/samples_stereo_subset

for i in {0..15}
do
  ./bin/generate_config_en.py \
      --sample_audio_path ./configs/resources/samples_stereo/sample.wav \
      --seed 777 \
      ./configs/resources/samples_stereo_subset/subset_${i} \
      ./configs/naturalness_MOS_sample_subset_${i}.yaml
done

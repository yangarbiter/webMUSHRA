#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import fnmatch
import os
import random

import yaml


def response_template():
    return [
        {
            "value": 1,
            "label": "1: とても不自然",
            "img": "configs/resources/images/star_off.png",
            "imgSelected": "configs/resources/images/star_on.png",
            "imgHigherResponseSelected": "configs/resources/images/star_on.png",
        },
        {
            "value": 2,
            "label": "2: やや不自然",
            "img": "configs/resources/images/star_off.png",
            "imgSelected": "configs/resources/images/star_on.png",
            "imgHigherResponseSelected": "configs/resources/images/star_on.png",
        },
        {
            "value": 3,
            "label": "3: 普通",
            "img": "configs/resources/images/star_off.png",
            "imgSelected": "configs/resources/images/star_on.png",
            "imgHigherResponseSelected": "configs/resources/images/star_on.png",
        },
        {
            "value": 4,
            "label": "4: やや自然",
            "img": "configs/resources/images/star_off.png",
            "imgSelected": "configs/resources/images/star_on.png",
            "imgHigherResponseSelected": "configs/resources/images/star_on.png",
        },
        {
            "value": 5,
            "label": "5: とても自然",
            "img": "configs/resources/images/star_off.png",
            "imgSelected": "configs/resources/images/star_on.png",
            "imgHigherResponseSelected": "configs/resources/images/star_on.png",
        },
    ]


def make_page(idx, total_idx, wav_path):
    wav_dir_id = os.path.basename(os.path.dirname(wav_path))
    wav_file_id = os.path.basename(wav_path)
    wav_id = f"{wav_dir_id}_{wav_file_id}"
    return {
        "type": "likert_single_stimulus",
        "id": wav_id,
        "content": "音声を聞いて、その自然性を5段階で評価してください。<br>"
                   "ここで自然性とは、<strong>音声がどれだけ人間の肉声に近いか</strong>を表し、<strong>人間の肉声が5</strong>に相当します。",
        "name": f"MOS on Naturalness ({idx}/{total_idx})",
        "mustRate": True,
        "mustPlayback": True,
        "reference": wav_path,
        "stimuli": {
            "C1": wav_path,
        },
        "response": response_template(),
    }


def make_first_page():
    return {
        "type": "generic",
        "content": "音声の自然性評価へようこそ。"
                   "<br>[Next]ボタンを押して次へ進んでください。",
        "id": "welcome",
        "name": "Audio naturalness evaluation",
    }


def make_volume_page(sample_wav_path):
    volume_page = {
        "type": "volume",
        "content": "音声を聞いて、適切なボリュームになるよう調整してください。<br>"
                   "<strong>静かな部屋</strong>で視聴を行い、必ず<strong>イヤホンもしくはヘッドホンを着用</strong>してください。<br>"
                   "もし、音声が再生されない場合は、更新ボタンを押してやり直してください。",
        "id": "Volume check",
        "stimulus": sample_wav_path,
        "defaultVolume": 1.0,
    }
    return volume_page


def make_finish_page():
    return {
        "type": "finish",
        "content": "評価が終了しました。<br>"
                   "あなたの名前を入力した後、[send Results]ボタンを押してください。",
        "id": "finish",
        "name": "Finshed evaluation",
        "popupContent": "評価が送信されました。ご協力ありがとうございました。",
        "showResults": False,
        "writeResults": True,
        "questionnaire": [
            {
                "type": "text",
                "label": "Name",
                "name": "name",
                "optional": False,
            },
        ]
    }


def find_files(root_dir, query="*.wav", include_root_dir=True):
    """Find files recursively.

    Args:
        root_dir (str): Root root_dir to find.
        query (str): Query to find.
        include_root_dir (bool): If False, root_dir name is not included.

    Returns:
        list: List of found filenames.

    """
    files = []
    for root, dirnames, filenames in os.walk(root_dir, followlinks=True):
        for filename in fnmatch.filter(filenames, query):
            files.append(os.path.join(root, filename))
    if not include_root_dir:
        files = [file_.replace(root_dir + "/", "") for file_ in files]

    return files


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--sample_audio_path", default=None, type=str)
    parser.add_argument("--seed", default=777, type=int)
    parser.add_argument("root_wav_dir")
    parser.add_argument("outpath")
    args = parser.parse_args()

    config = {
        "testname": "MOS on Naturalness",
        "testId": "mos_on_naturalness",
        "bufferSize": 2048,
        "stopOnErrors": True,
        "showButtonPreviousPage": False,
        "remoteService": "service/write.php",
        "pages": [],
    }

    wav_path_list = sorted(find_files(args.root_wav_dir))
    random.seed(args.seed)
    random.shuffle(wav_path_list)
    config["pages"] += [make_first_page()]
    if args.sample_audio_path is not None:
        config["pages"] += [make_volume_page(args.sample_audio_path)]
    for idx, wav_path in enumerate(wav_path_list, 1):
        config["pages"] += [make_page(idx, len(wav_path_list), wav_path)]
    config["pages"] += [make_finish_page()]

    with open(args.outpath, "w") as f:
        yaml.safe_dump(config, f, allow_unicode=True, encoding="utf-8")


if __name__ == "__main__":
    main()

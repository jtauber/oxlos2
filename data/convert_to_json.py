#!/usr/bin/env python3

import json
import os.path


def convert():
    directory = os.path.dirname(os.path.abspath(__file__))
    filename = os.path.join(directory, "mis-parse.txt")

    with open(filename) as f:

        items = []

        for line in f:
            ccat, jtauber, form, lemma = line.strip().split()
            jtauber_list = jtauber.split("/")
            choices = [ccat, *jtauber_list]
            item = {
                "question": {
                    "lemma": lemma,
                    "form": form,
                },
                "choices": choices,
            }
            items.append(item)

    return items

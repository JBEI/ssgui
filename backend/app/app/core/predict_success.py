#!/usr/bin/env python

import io
import zipfile


def predict_sample_success(input1, input2) -> io.BytesIO:
    zip_results = io.BytesIO()
    with zipfile.ZipFile(zip_results, "w") as archive:
        archive.writestr(
            "hello/random.txt",
            "hi :p",
        )
    zip_results.seek(0)
    return zip_results

"""Klasifikasi prioritas tiket IT Helpdesk (Rendah/Sedang/Tinggi).
Algoritme: TF-IDF + Multinomial Naive Bayes. Jalankan di Google Colab.
Prasyarat: unggah dataset_tiket_ti.csv ke sesi Colab.
"""
import re
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import (train_test_split, StratifiedKFold,
                                     cross_val_score)
from sklearn.naive_bayes import MultinomialNB
from sklearn.linear_model import LogisticRegression
from sklearn.svm import LinearSVC
from sklearn.pipeline import Pipeline
from sklearn.metrics import (accuracy_score, classification_report,
                             confusion_matrix)

SEED = 42
df = pd.read_csv("dataset_tiket_ti.csv")


# 1. Pra-pemrosesan teks
def bersihkan(t):
    t = t.lower()
    t = re.sub(r"[^a-z0-9\s]", " ", t)
    return re.sub(r"\s+", " ", t).strip()


STOP = {"di", "yang", "dan", "ke", "dari", "untuk", "saya", "mohon",
        "tolong", "ada", "ini", "itu", "dengan", "pada", "sudah",
        "atau", "agar", "halo", "selamat", "siang", "tim", "ti",
        "bantuan"}


def tok(t):
    return [w for w in bersihkan(t).split() if w not in STOP]


df["bersih"] = df["deskripsi"].apply(bersihkan)

# 2. Pembagian data 80:20 berstrata
X_tr, X_te, y_tr, y_te = train_test_split(
    df["bersih"], df["prioritas"], test_size=0.2,
    stratify=df["prioritas"], random_state=SEED)


# 3. Pipeline: TF-IDF (unigram+bigram) -> classifier
def buat_model(clf, ngram=(1, 2)):
    tfidf = TfidfVectorizer(tokenizer=tok, token_pattern=None,
                            ngram_range=ngram, sublinear_tf=True)
    return Pipeline([("tfidf", tfidf), ("clf", clf)])


model = buat_model(MultinomialNB(alpha=0.1)).fit(X_tr, y_tr)
pred = model.predict(X_te)

# 4. Evaluasi hold-out
labels = ["Rendah", "Sedang", "Tinggi"]
print("Akurasi uji:", accuracy_score(y_te, pred))
print(classification_report(y_te, pred, digits=3))
print(confusion_matrix(y_te, pred, labels=labels))

# 5. Validasi silang 5 lipatan
skf = StratifiedKFold(5, shuffle=True, random_state=SEED)
cv = cross_val_score(buat_model(MultinomialNB(alpha=0.1)),
                     df["bersih"], df["prioritas"], cv=skf)
print("CV:", cv.round(3), "rerata", cv.mean().round(3))

# 6. Perbandingan algoritme
for nama, clf in [("Naive Bayes", MultinomialNB(alpha=0.1)),
                  ("Logistic Regression",
                   LogisticRegression(max_iter=1000, C=10)),
                  ("Linear SVM", LinearSVC(C=1.0))]:
    s = cross_val_score(buat_model(clf), df["bersih"],
                        df["prioritas"], cv=skf)
    print(f"{nama}: {s.mean():.3f} +/- {s.std():.3f}")

# 7. Aturan keputusan: ambang kepercayaan + kata kunci keamanan
nb = model.named_steps["clf"]
KUNCI = ["peretasan", "diretas", "phishing", "ransomware", "bocor",
         "serangan", "malware", "mencurigakan"]


def putuskan(teks, ambang=0.70):
    p = model.predict_proba([bersihkan(teks)])[0]
    kelas, conf = nb.classes_[p.argmax()], float(p.max())
    if conf < ambang or any(k in teks.lower() for k in KUNCI):
        return kelas, conf, "TINJAU PETUGAS"
    return kelas, conf, "OTOMATIS"


# 8. Demonstrasi tiket baru
baru = [
    "server SIAKAD tidak bisa diakses semua mahasiswa saat pengisian KRS",
    "printer di ruang dosen macet kertasnya",
    "mohon bantuan reset password email kampus",
    "wifi lantai 3 putus dan ada indikasi serangan siber",
    "minta panduan penggunaan e-learning untuk mahasiswa baru",
    "laptop saya lambat sekali",
]
for t in baru:
    print(t, "->", putuskan(t))

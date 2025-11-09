# ...existing code...
import streamlit as st
import math
import itertools
from collections import Counter

st.set_page_config(page_title="순열 계산기", layout="wide")

st.title("🔢 순열 계산기")
st.write("모드별로 입력을 설정한 후 '계산' 버튼을 눌러 경우의 수와 실제 나열을 확인하세요.")

mode = st.selectbox("모드 선택", [
    "1) 일반 순열 (서로 다른 n개에서 k개 뽑아 순서있게, 중복 없음)",
    "2) 중복(반복) 순열 (서로 다른 n개에서 k개 뽑아 순서있게, 중복 허용)",
    "3) 같은 것이 있는 순열 (각 아이템별 개수가 주어졌을 때 전체 순열)"
])

max_display = st.number_input("화면에 표시할 최대 경우 수 (권장 1000 이하)", min_value=10, max_value=20000, value=1000, step=10)

def factorial(n):
    return math.factorial(n)

def multiset_permutations(counter):
    # counter: Counter({elem: count, ...})
    total = sum(counter.values())
    if total == 0:
        yield ()
        return
    for elem in list(counter.keys()):
        if counter[elem] <= 0:
            continue
        counter[elem] -= 1
        for rest in multiset_permutations(counter):
            yield (elem,) + rest
        counter[elem] += 1

def format_perm(p):
    return " ".join(map(str, p))

if mode.startswith("1)"):
    st.subheader("일반 순열 (중복 없음)")
    n = st.number_input("총 항목 수 n (각 항목은 서로 다름)", min_value=1, value=5, step=1)
    k = st.number_input("뽑을 개수 k", min_value=0, value=min(3, int(n)), max_value=int(n), step=1)
    labels_input = st.text_input("항목 레이블 (콤마로 구분, 비워두면 자동 A,B,C...)", value="")
    if labels_input.strip():
        labels = [s.strip() for s in labels_input.split(",")][:int(n)]
        if len(labels) < n:
            # pad
            labels += [f"X{i}" for i in range(len(labels)+1, int(n)+1)]
    else:
        labels = [chr(65 + i) for i in range(int(n))]

    if st.button("계산"):
        if k > n:
            st.error("k는 n보다 클 수 없습니다.")
        else:
            total = math.perm(int(n), int(k)) if hasattr(math, "perm") else factorial(int(n)) // factorial(int(n) - int(k))
            st.success(f"총 경우의 수: {total}")
            if total > max_display:
                st.warning(f"경고: 총 {total}개 중 앞 {max_display}개만 표시합니다.")
            shown = 0
            for p in itertools.permutations(labels, int(k)):
                if shown >= max_display:
                    break
                st.text(format_perm(p))
                shown += 1

elif mode.startswith("2)"):
    st.subheader("중복(반복) 순열")
    n = st.number_input("서로 다른 항목 수 n", min_value=1, value=3, step=1)
    k = st.number_input("뽑을 개수 k", min_value=0, value=3, step=1)
    labels_input = st.text_input("항목 레이블 (콤마로 구분, 비워두면 자동 A,B,C...)", value="")
    if labels_input.strip():
        labels = [s.strip() for s in labels_input.split(",")][:int(n)]
        if len(labels) < n:
            labels += [f"X{i}" for i in range(len(labels)+1, int(n)+1)]
    else:
        labels = [chr(65 + i) for i in range(int(n))]

    if st.button("계산"):
        total = (int(n) ** int(k))
        st.success(f"총 경우의 수: {total}")
        if total > max_display:
            st.warning(f"경고: 총 {total}개 중 앞 {max_display}개만 표시합니다.")
        shown = 0
        for p in itertools.product(labels, repeat=int(k)):
            if shown >= max_display:
                break
            st.text(format_perm(p))
            shown += 1

else:
    st.subheader("같은 것이 있는 순열 (멀티셋 순열)")
    m = st.number_input("서로 다른 항목 종류 수", min_value=1, value=3, step=1)
    with st.form(key="multiset_form"):
        cols = st.columns(3)
        labels = []
        counts = []
        for i in range(int(m)):
            with cols[i % 3]:
                lab = st.text_input(f"항목 {i+1} 레이블", value=f"A{i+1}", key=f"lab{i}")
                cnt = st.number_input(f"항목 {i+1} 개수", min_value=0, value=1, key=f"cnt{i}")
            labels.append(lab)
            counts.append(int(cnt))
        submitted = st.form_submit_button("계산")

    if 'submitted' in locals() and submitted:
        total_items = sum(counts)
        if total_items == 0:
            st.error("총 항목 수가 0입니다.")
        else:
            denom = 1
            for c in counts:
                denom *= factorial(c)
            total = factorial(total_items) // denom
            st.success(f"총 경우의 수: {total} (총 항목 수: {total_items})")
            if total > max_display:
                st.warning(f"경고: 총 {total}개 중 앞 {max_display}개만 표시합니다.")
            counter = Counter()
            for lab, c in zip(labels, counts):
                if c > 0:
                    counter[lab] = c
            shown = 0
            for p in multiset_permutations(counter):
                if shown >= max_display:
                    break
                st.text(format_perm(p))
                shown += 1

st.caption("Streamlit 앱 실행: 터미널에서 'streamlit run streamlit_app.py' 실행")
# ...existing code...
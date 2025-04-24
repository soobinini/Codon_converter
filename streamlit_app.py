import streamlit as st
import time

# RNA 코돈 테이블
codon_table = {
    'AUG': 'M', 'UUU': 'F', 'UUC': 'F', 'UUA': 'L', 'UUG': 'L',
    'UCU': 'S', 'UCC': 'S', 'UCA': 'S', 'UCG': 'S',
    'UAU': 'Y', 'UAC': 'Y', 'UGU': 'C', 'UGC': 'C',
    'UGG': 'W', 'CUU': 'L', 'CUC': 'L', 'CUA': 'L', 'CUG': 'L',
    'CCU': 'P', 'CCC': 'P', 'CCA': 'P', 'CCG': 'P',
    'CAU': 'H', 'CAC': 'H', 'CAA': 'Q', 'CAG': 'Q',
    'CGU': 'R', 'CGC': 'R', 'CGA': 'R', 'CGG': 'R',
    'AUU': 'I', 'AUC': 'I', 'AUA': 'I', 'ACU': 'T',
    'ACC': 'T', 'ACA': 'T', 'ACG': 'T', 'AAU': 'N',
    'AAC': 'N', 'AAA': 'K', 'AAG': 'K', 'AGU': 'S',
    'AGC': 'S', 'AGA': 'R', 'AGG': 'R', 'GUU': 'V',
    'GUC': 'V', 'GUA': 'V', 'GUG': 'V', 'GCU': 'A',
    'GCC': 'A', 'GCA': 'A', 'GCG': 'A', 'GAU': 'D',
    'GAC': 'D', 'GAA': 'E', 'GAG': 'E', 'GGU': 'G',
    'GGC': 'G', 'GGA': 'G', 'GGG': 'G',
    'UAA': '*', 'UAG': '*', 'UGA': '*'
}

start_codon = 'AUG'
stop_codons = {'UAA', 'UAG', 'UGA'}

st.set_page_config(page_title="RNA 번역기", page_icon="🧬")
st.title("🧬 RNA → 아미노산 변환 시각화기")
st.markdown("**RNA 염기서열**을 입력하면, 코돈 단위로 번역하여 아미노산으로 변환합니다.")

rna_input = st.text_input("RNA 염기서열을 입력하세요 (예: `AUGGCCUAA`)").upper()

# 유효성 검사
if rna_input and any(base not in 'AUCG' for base in rna_input):
    st.error("⚠ RNA는 A, U, C, G 염기로만 구성되어야 합니다.")
elif rna_input:
    codons = [rna_input[i:i+3] for i in range(0, len(rna_input), 3)]
    started = False
    ended = False

    container = st.container()
    with container:
        st.subheader("🔍 번역 진행")

        placeholder = st.empty()

        for codon in codons:
            if len(codon) < 3:
                continue  # 마지막 불완전 코돈 무시

            if not started:
                if codon == start_codon:
                    started = True
                    placeholder.info(f"🟢 시작 코돈 `{codon}` 발견 — 번역 시작합니다!")
                    time.sleep(1)
                else:
                    continue

            if started:
                if codon in stop_codons:
                    placeholder.error(f"🛑 종결 코돈 `{codon}` 발견 — 번역 종료")
                    st.code(" ".join(codons), language='text')
                    break

                amino = codon_table.get(codon, '?')
                with st.container():
                    st.markdown(f"""
                        <div style="padding:10px; border-radius:10px; background-color:#e8f5e9; margin-bottom:10px;">
                            <strong>코돈:</strong> <code>{codon}</code> → 
                            <strong>아미노산:</strong> <span style="color:green; font-weight:bold;">{amino}</span>
                        </div>
                    """, unsafe_allow_html=True)
                time.sleep(0.6)

        if started and codons[-1] not in stop_codons:
            st.warning("⚠ 번역이 시작되었지만 종결 코돈이 없어 끝나지 않았습니다.")
    st.success("✅ 번역 완료")

##### 기본 정보 불러오기 ####
# Streamlit 패키지 추가
import streamlit as st
# OpenAI 패키기 추가
import openai

##### 기능 구현 함수 #####
def askGpt(prompt,apikey):
    # 프롬프트를 input으로 받아서 양식으로 변경시켜줘서 변수에 저장 
    client = openai.OpenAI(api_key = apikey)
    # gpt에서 받은 응답을 response에 저장 
    response = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[{"role": "user", "content": prompt}])
    # response에서 응답 부분만 발췌해서 gptResposne에 저장해서 리턴함
    gptResponse = response.choices[0].message.content
    return gptResponse

##### 메인 함수 #####
def main():
    # 페이지 타이틀 생성하기 (크롬막대기 위쪽에 생기는거)
    st.set_page_config(page_title="요약 프로그램")
    # session state 초기화
    if "OPENAI_API" not in st.session_state:
        st.session_state["OPENAI_API"] = ""

    # 사이드바
    with st.sidebar:
        # Open AI API 키 입력받기 (타입을 패스워드로 지정해서 뭘 입력해도 노출이 되지 않음)
        open_apikey = st.text_input(label='OPENAI API 키', placeholder='Enter Your API Key', value='',type='password')    
        # 입력받은 API 키 표시(텍스트 입력받으면 if문 동작 -> 더이상 api 키 입력할 필요가 없어짐)
        if open_apikey:
            st.session_state["OPENAI_API"] = open_apikey
        # 구분선 생성해주기
        st.markdown('---')

    # 프로그램의 제목을 입력해줌
    st.header("📃요약 프로그램")
    st.markdown('---')
    
    # text_input엘리멘트와는 다르게 text_area는 좀 더 넓은 공간에서 텍스트를 입력받을 수 있음
    # 유저가 직접 높이 조절 가능함
    text = st.text_area("요약 할 글을 입력하세요")

    # 요약 버튼을 누를 경우 if문 실행됨
    # 여기에 작성된 prompt부분은 챗지피티에게 요약을 최대한 잘해달라고 요청하는
    # 시스템 프롬프트 (일종의 프롬프트 엔지니어링 과정)->좀 더 퀄리티있는결과
    # 프롬프트 내용 : 지침들을 작성하고 강조할 내용 작성함
    if st.button("요약"):
        prompt = f'''
        **Instructions** :
    - You are an expert assistant that summarizes text into **Korean language**.
    - Your task is to summarize the **text** sentences in **Korean language**.
    - Your summaries should include the following :
        - Omit duplicate content, but increase the summary weight of duplicate content.
        - Summarize by emphasizing concepts and arguments rather than case evidence.
        - Summarize in 3 lines.
        - Use the format of a bullet point.
    -text : {text}
    '''
        st.info(askGpt(prompt,st.session_state["OPENAI_API"]))
    # st.info를 사요하면 이쁜 네모 박스로 텍스트 표현이 가능함
    # 파란색 아니어도 다른 색깔로도 표현 가능함 (streamlit사이트에서 확인)
if __name__=="__main__":
    main()

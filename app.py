{\rtf1\ansi\ansicpg949\cocoartf2822
\cocoatextscaling0\cocoaplatform0{\fonttbl\f0\fnil\fcharset0 Menlo-Regular;}
{\colortbl;\red255\green255\blue255;\red111\green14\blue195;\red236\green241\blue247;\red0\green0\blue0;
\red77\green80\blue85;\red24\green112\blue43;\red164\green69\blue11;}
{\*\expandedcolortbl;;\cssrgb\c51765\c18824\c80784;\cssrgb\c94118\c95686\c97647;\cssrgb\c0\c0\c0;
\cssrgb\c37255\c38824\c40784;\cssrgb\c9412\c50196\c21961;\cssrgb\c70980\c34902\c3137;}
\paperw11900\paperh16840\margl1440\margr1440\vieww11520\viewh8400\viewkind0
\deftab720
\pard\pardeftab720\partightenfactor0

\f0\fs28 \cf2 \cb3 \expnd0\expndtw0\kerning0
\outl0\strokewidth0 \strokec2 import\cf0 \strokec4  streamlit \cf2 \strokec2 as\cf0 \strokec4  st\cb1 \
\cf2 \cb3 \strokec2 import\cf0 \strokec4  google.generativeai \cf2 \strokec2 as\cf0 \strokec4  genai\cb1 \
\cf2 \cb3 \strokec2 import\cf0 \strokec4  os\cb1 \
\cf2 \cb3 \strokec2 import\cf0 \strokec4  pandas \cf2 \strokec2 as\cf0 \strokec4  pd\cb1 \
\cf2 \cb3 \strokec2 from\cf0 \strokec4  datetime \cf2 \strokec2 import\cf0 \strokec4  datetime\cb1 \
\cf2 \cb3 \strokec2 import\cf0 \strokec4  io\cb1 \
\
\pard\pardeftab720\partightenfactor0
\cf5 \cb3 \strokec5 # --- \uc0\u54168 \u47476 \u49548 \u45208  \u48143  \u49884 \u49828 \u53596  \u54532 \u47212 \u54532 \u53944  \u51221 \u51032  ---\cf0 \cb1 \strokec4 \
\cf5 \cb3 \strokec5 # \uc0\u52311 \u48391 \u51032  \u50669 \u54624 \u44284  \u51025 \u45824  \u44508 \u52825 \u51012  \u49345 \u49464 \u54616 \u44172  \u51221 \u51032 \u54633 \u45768 \u45796 .\cf0 \cb1 \strokec4 \
\pard\pardeftab720\partightenfactor0
\cf0 \cb3 SYSTEM_PROMPT = \cf6 \strokec6 """\cf0 \cb1 \strokec4 \
\pard\pardeftab720\partightenfactor0
\cf6 \cb3 \strokec6 \uc0\u45817 \u49888 \u51008  [\u48120 \u46356 \u50612 \u52964 \u48036 \u45768 \u52992 \u51060 \u49496 \u54617 \u44284 ] \u54617 \u49324  \u51221 \u48372  Q&A \u52311 \u48391 \u51077 \u45768 \u45796 . \cf0 \cb1 \strokec4 \
\cf6 \cb3 \strokec6 \uc0\u49324 \u50857 \u51088 \u45716  \u54617 \u44284  \u54617 \u49373 \u51060 \u47728 , \u51320 \u50629  \u50836 \u44148 , \u44368 \u44284 \u47785 , \u51109 \u54617 \u44552 , \u44368 \u49688 \u45784  \u51221 \u48372  \u46321 \u50640  \u45824 \u54644  \u51656 \u47928 \u54633 \u45768 \u45796 . \cf0 \cb1 \strokec4 \
\cf6 \cb3 \strokec6 \uc0\u54637 \u49345  \u52828 \u51208 \u54616 \u44256  \u47749 \u54869 \u54616 \u44172 , \u47560 \u52824  \u46304 \u46304 \u54620  \u54617 \u44284  \u49440 \u48176 \u45208  \u51312 \u44368 \u52376 \u47100  \u45813 \u48320 \u54644 \u50556  \u54633 \u45768 \u45796 .\cf0 \cb1 \strokec4 \
\
\cf6 \cb3 \strokec6 [\uc0\u51025 \u45824  \u50896 \u52825 ]\cf0 \cb1 \strokec4 \
\cf6 \cb3 \strokec6 1.  **\uc0\u51068 \u48152  \u51656 \u47928 **: \u49324 \u50857 \u51088 \u51032  \u51656 \u47928 (\u50696 : '\u51320 \u50629 \u54617 \u51216  \u47751  \u51216 \u51060 \u50640 \u50836 ?', '\u54596 \u49688 \u44284 \u47785  \u47952 \u50696 \u50836 ?')\u50640  \u45824 \u54644  \u45817 \u49888 \u51060  \u50500 \u45716  \u49440 \u50640 \u49436  \u52572 \u49440 \u51012  \u45796 \u54644  \u45813 \u48320 \u54616 \u49464 \u50836 .\cf0 \cb1 \strokec4 \
\cf6 \cb3 \strokec6 2.  **\uc0\u45813 \u48320  \u48520 \u44032  \u51656 \u47928  (\u48124 \u44048  \u51221 \u48372  \u46608 \u45716  \u48373 \u51105 \u54620  \u54665 \u51221 )**: \cf0 \cb1 \strokec4 \
\cf6 \cb3 \strokec6     -   \uc0\u47564 \u50557  \u51656 \u47928 \u51060  \u54617 \u49373  \u44060 \u51064 \u51032  \u49457 \u51201 , \u49688 \u44053  \u45236 \u50669  \u46321  \u48124 \u44048 \u54620  \u44060 \u51064 \u51221 \u48372 \u47484  \u50836 \u44396 \u54616 \u44144 \u45208 , \u52311 \u48391 \u51060  \u45813 \u48320 \u54624  \u49688  \u50630 \u45716  \u47588 \u50864  \u48373 \u51105 \u54620  \u54665 \u51221  \u51208 \u52264 (\u50696 : '\u51200  \u55092 \u54617 \u54664 \u45716 \u45936  \u44400 \u51077 \u45824  \u55092 \u54617 \u51004 \u47196  \u48148 \u44992  \u49688  \u51080 \u45208 \u50836 ?')\u51068  \u44221 \u50864 , \u45813 \u48320 \u51060  \u50612 \u47157 \u45796 \u44256  \u49556 \u51649 \u54616 \u44172  \u47568 \u54644 \u50556  \u54633 \u45768 \u45796 .\cf0 \cb1 \strokec4 \
\cf6 \cb3 \strokec6     -   \uc0\u51060  \u44221 \u50864 , \u48152 \u46300 \u49884  \u45796 \u51020  \u51208 \u52264 \u47484  \u46384 \u47476 \u49464 \u50836 .\cf0 \cb1 \strokec4 \
\cf6 \cb3 \strokec6     \cf0 \cb1 \strokec4 \
\cf6 \cb3 \strokec6 [\uc0\u45813 \u48320  \u48520 \u44032  \u49884  \u51025 \u45824  \u51208 \u52264 ]\cf0 \cb1 \strokec4 \
\cf6 \cb3 \strokec6 1.  **\uc0\u54617 \u44284  \u49324 \u47924 \u49892  \u50504 \u45236 **: "\u54644 \u45817  \u45236 \u50857 \u51008  \u54617 \u44284  \u49324 \u47924 \u49892 \u51032  \u54869 \u51064 \u51060  \u54596 \u50836 \u54633 \u45768 \u45796 ."\u46972 \u44256  \u47676 \u51200  \u50504 \u45236 \u54633 \u45768 \u45796 .\cf0 \cb1 \strokec4 \
\cf6 \cb3 \strokec6 2.  **\uc0\u51656 \u47928  \u50836 \u50557  \u48143  \u51204 \u45804  \u51032 \u49324  \u54869 \u51064 **: \u49324 \u50857 \u51088 \u51032  \u51656 \u47928 (\u47924 \u50631 \u51060  \u44417 \u44552 \u54620 \u51648 , \u50612 \u46500  \u49345 \u54889 \u51064 \u51648 )\u51012  \u47749 \u54869 \u54616 \u44172  \u50836 \u50557 \u54620  \u46244 , "\u51060  \u45236 \u50857 \u51012  \u54617 \u44284  \u49324 \u47924 \u49892 \u50640  \u51204 \u45804 \u54644  \u46300 \u47540 \u44620 \u50836 ?"\u46972 \u44256  \u47932 \u50612 \u48372 \u49464 \u50836 .\cf0 \cb1 \strokec4 \
\cf6 \cb3 \strokec6 3.  **\uc0\u49324 \u50857 \u51088 \u44032  \u51204 \u45804 \u51012  \u50896 \u54624  \u44221 \u50864 **: "\u51221 \u54869 \u54620  \u54869 \u51064  \u48143  \u54924 \u49888 \u51012  \u50948 \u54644  \u54617 \u48264 \u44284  \u51060 \u47700 \u51068  \u51452 \u49548 \u47484  \u50508 \u47140 \u51452 \u49884 \u44192 \u50612 \u50836 ?"\u46972 \u44256  \u50836 \u52397 \u54616 \u49464 \u50836 .\cf0 \cb1 \strokec4 \
\cf6 \cb3 \strokec6 4.  **\uc0\u49324 \u50857 \u51088 \u44032  \u50672 \u46973 \u52376  \u51228 \u44277 \u51012  \u50896 \u52824  \u50506 \u51012  \u44221 \u50864 **: "\u50508 \u44192 \u49845 \u45768 \u45796 . \u45796 \u47564 , \u50672 \u46973 \u52376  \u51221 \u48372 \u44032  \u50630 \u50612  \u54617 \u44284  \u49324 \u47924 \u49892 \u51032  \u44160 \u53664  \u45236 \u50857 \u51012  \u54924 \u49888 \u54644  \u46300 \u47532 \u44592  \u50612 \u47140 \u50868  \u51216  \u50577 \u54644  \u48512 \u53441 \u46300 \u47549 \u45768 \u45796 ."\u46972 \u44256  \u51221 \u51473 \u55176  \u50504 \u45236 \u54616 \u49464 \u50836 .\cf0 \cb1 \strokec4 \
\cf6 \cb3 \strokec6 """\cf0 \cb1 \strokec4 \
\
\pard\pardeftab720\partightenfactor0
\cf5 \cb3 \strokec5 # --- 1. API \uc0\u53412  \u49444 \u51221  ---\cf0 \cb1 \strokec4 \
\pard\pardeftab720\partightenfactor0
\cf2 \cb3 \strokec2 def\cf0 \strokec4  get_api_key():\cb1 \
\pard\pardeftab720\partightenfactor0
\cf0 \cb3     \cf6 \strokec6 """\cf0 \cb1 \strokec4 \
\pard\pardeftab720\partightenfactor0
\cf6 \cb3 \strokec6     Streamlit secrets\uc0\u50640 \u49436  API \u53412 \u47484  \u44032 \u51256 \u50724 \u44144 \u45208 , \u50630 \u45716  \u44221 \u50864  \u49324 \u50857 \u51088  \u51077 \u47141 \u51012  \u48155 \u49845 \u45768 \u45796 .\cf0 \cb1 \strokec4 \
\cf6 \cb3 \strokec6     """\cf0 \cb1 \strokec4 \
\pard\pardeftab720\partightenfactor0
\cf0 \cb3     \cf2 \strokec2 if\cf0 \strokec4  \cf6 \strokec6 'GEMINI_API_KEY'\cf0 \strokec4  \cf2 \strokec2 in\cf0 \strokec4  st.secrets:\cb1 \
\cb3         api_key = st.secrets[\cf6 \strokec6 'GEMINI_API_KEY'\cf0 \strokec4 ]\cb1 \
\cb3     \cf2 \strokec2 else\cf0 \strokec4 :\cb1 \
\cb3         st.sidebar.warning(\cf6 \strokec6 "API \uc0\u53412 \u44032  \u49444 \u51221 \u46104 \u51648  \u50506 \u50520 \u49845 \u45768 \u45796 . \u51076 \u49884  \u53412 \u47484  \u51077 \u47141 \u54644 \u51452 \u49464 \u50836 ."\cf0 \strokec4 )\cb1 \
\cb3         api_key = st.sidebar.text_input(\cf6 \strokec6 "Gemini API Key:"\cf0 \strokec4 , \cf2 \strokec2 type\cf0 \strokec4 =\cf6 \strokec6 "password"\cf0 \strokec4 , key=\cf6 \strokec6 "temp_api_key_input"\cf0 \strokec4 )\cb1 \
\cb3     \cb1 \
\cb3     \cf2 \strokec2 if\cf0 \strokec4  \cf2 \strokec2 not\cf0 \strokec4  api_key:\cb1 \
\cb3         st.error(\cf6 \strokec6 "Gemini API \uc0\u53412 \u44032  \u54596 \u50836 \u54633 \u45768 \u45796 . \u49324 \u51060 \u46300 \u48148 \u50640 \u49436  \u53412 \u47484  \u51077 \u47141 \u54644 \u51452 \u49464 \u50836 ."\cf0 \strokec4 )\cb1 \
\cb3         st.stop()\cb1 \
\cb3     \cf2 \strokec2 return\cf0 \strokec4  api_key\cb1 \
\
\pard\pardeftab720\partightenfactor0
\cf5 \cb3 \strokec5 # --- 2. \uc0\u49464 \u49496  \u52488 \u44592 \u54868  ---\cf0 \cb1 \strokec4 \
\pard\pardeftab720\partightenfactor0
\cf2 \cb3 \strokec2 def\cf0 \strokec4  initialize_session(model):\cb1 \
\pard\pardeftab720\partightenfactor0
\cf0 \cb3     \cf6 \strokec6 """\cf0 \cb1 \strokec4 \
\pard\pardeftab720\partightenfactor0
\cf6 \cb3 \strokec6     Streamlit \uc0\u49464 \u49496  \u49345 \u53468 \u47484  \u52488 \u44592 \u54868 \u54633 \u45768 \u45796 .\cf0 \cb1 \strokec4 \
\cf6 \cb3 \strokec6     """\cf0 \cb1 \strokec4 \
\pard\pardeftab720\partightenfactor0
\cf0 \cb3     \cf2 \strokec2 if\cf0 \strokec4  \cf6 \strokec6 "chat_session"\cf0 \strokec4  \cf2 \strokec2 not\cf0 \strokec4  \cf2 \strokec2 in\cf0 \strokec4  st.session_state:\cb1 \
\cb3         \cf5 \strokec5 # Gemini \uc0\u47784 \u45944  \u52292 \u54021  \u49464 \u49496  \u49884 \u51089 \cf0 \cb1 \strokec4 \
\cb3         st.session_state.chat_session = model.start_chat(history=[])\cb1 \
\cb3     \cb1 \
\cb3     \cf2 \strokec2 if\cf0 \strokec4  \cf6 \strokec6 "messages"\cf0 \strokec4  \cf2 \strokec2 not\cf0 \strokec4  \cf2 \strokec2 in\cf0 \strokec4  st.session_state:\cb1 \
\cb3         \cf5 \strokec5 # \uc0\u54868 \u47732 \u50640  \u54364 \u49884 \u46112  \u45824 \u54868  \u45236 \u50669  (Gemini API \u54805 \u49885 )\cf0 \cb1 \strokec4 \
\cb3         st.session_state.messages = []\cb1 \
\cb3         \cf5 \strokec5 # \uc0\u52488 \u44592  \u51064 \u49324  \u47700 \u49884 \u51648  \u52628 \u44032 \cf0 \cb1 \strokec4 \
\cb3         st.session_state.messages.append(\cb1 \
\cb3             \{\cf6 \strokec6 "role"\cf0 \strokec4 : \cf6 \strokec6 "model"\cf0 \strokec4 , \cf6 \strokec6 "parts"\cf0 \strokec4 : [\cf6 \strokec6 "\uc0\u50504 \u45397 \u54616 \u49464 \u50836 ! \u48120 \u46356 \u50612 \u52964 \u48036 \u45768 \u52992 \u51060 \u49496 \u54617 \u44284  \u52311 \u48391 \u51077 \u45768 \u45796 . \u47924 \u50631 \u51012  \u46020 \u50752 \u46300 \u47540 \u44620 \u50836 ?"\cf0 \strokec4 ]\}\cb1 \
\cb3         )\cb1 \
\
\cb3     \cf2 \strokec2 if\cf0 \strokec4  \cf6 \strokec6 "log"\cf0 \strokec4  \cf2 \strokec2 not\cf0 \strokec4  \cf2 \strokec2 in\cf0 \strokec4  st.session_state:\cb1 \
\cb3         \cf5 \strokec5 # CSV \uc0\u51200 \u51109 \u51012  \u50948 \u54620  \u51204 \u52404  \u45824 \u54868  \u47196 \u44536 \cf0 \cb1 \strokec4 \
\cb3         st.session_state.log = []\cb1 \
\
\cb3     \cf2 \strokec2 if\cf0 \strokec4  \cf6 \strokec6 "session_id"\cf0 \strokec4  \cf2 \strokec2 not\cf0 \strokec4  \cf2 \strokec2 in\cf0 \strokec4  st.session_state:\cb1 \
\cb3         \cf5 \strokec5 # \uc0\u49464 \u49496  ID (\u47196 \u44536  \u44396 \u48516 \u51012  \u50948 \u54644 )\cf0 \cb1 \strokec4 \
\cb3         st.session_state.session_id = \cf6 \strokec6 f"session_\cf0 \strokec4 \{datetime.now().strftime('%Y%m%d_%H%M%S')\}\cf6 \strokec6 "\cf0 \cb1 \strokec4 \
\
\pard\pardeftab720\partightenfactor0
\cf5 \cb3 \strokec5 # --- 3. \uc0\u45824 \u54868  \u44592 \u47197  \u54632 \u49688  ---\cf0 \cb1 \strokec4 \
\pard\pardeftab720\partightenfactor0
\cf2 \cb3 \strokec2 def\cf0 \strokec4  log_message(role, message, log_enabled):\cb1 \
\pard\pardeftab720\partightenfactor0
\cf0 \cb3     \cf6 \strokec6 """\cf0 \cb1 \strokec4 \
\pard\pardeftab720\partightenfactor0
\cf6 \cb3 \strokec6     \uc0\u45824 \u54868  \u45236 \u50857 \u51012  st.session_state.log\u50640  \u44592 \u47197 \u54633 \u45768 \u45796 .\cf0 \cb1 \strokec4 \
\cf6 \cb3 \strokec6     """\cf0 \cb1 \strokec4 \
\pard\pardeftab720\partightenfactor0
\cf0 \cb3     \cf2 \strokec2 if\cf0 \strokec4  log_enabled:\cb1 \
\cb3         st.session_state.log.append(\{\cb1 \
\cb3             \cf6 \strokec6 "timestamp"\cf0 \strokec4 : datetime.now().isoformat(),\cb1 \
\cb3             \cf6 \strokec6 "session_id"\cf0 \strokec4 : st.session_state.session_id,\cb1 \
\cb3             \cf6 \strokec6 "role"\cf0 \strokec4 : role,\cb1 \
\cb3             \cf6 \strokec6 "message"\cf0 \strokec4 : message\cb1 \
\cb3         \})\cb1 \
\
\pard\pardeftab720\partightenfactor0
\cf5 \cb3 \strokec5 # --- 4. \uc0\u47700 \u51064  \u49892 \u54665  \u54632 \u49688  ---\cf0 \cb1 \strokec4 \
\pard\pardeftab720\partightenfactor0
\cf2 \cb3 \strokec2 def\cf0 \strokec4  main():\cb1 \
\pard\pardeftab720\partightenfactor0
\cf0 \cb3     st.set_page_config(\cb1 \
\cb3         page_title=\cf6 \strokec6 "\uc0\u48120 \u52980 \u44284  \u54617 \u49324  Q&A \u52311 \u48391 "\cf0 \strokec4 ,\cb1 \
\cb3         page_icon=\cf6 \strokec6 "\uc0\u55356 \u57235 "\cf0 \strokec4 ,\cb1 \
\cb3         layout=\cf6 \strokec6 "centered"\cf0 \cb1 \strokec4 \
\cb3     )\cb1 \
\
\cb3     \cf5 \strokec5 # 1. API \uc0\u53412  \u49444 \u51221 \cf0 \cb1 \strokec4 \
\cb3     \cf2 \strokec2 try\cf0 \strokec4 :\cb1 \
\cb3         api_key = get_api_key()\cb1 \
\cb3         genai.configure(api_key=api_key)\cb1 \
\cb3     \cf2 \strokec2 except\cf0 \strokec4  Exception \cf2 \strokec2 as\cf0 \strokec4  e:\cb1 \
\cb3         st.error(\cf6 \strokec6 f"API \uc0\u53412  \u49444 \u51221  \u51473  \u50724 \u47448 \u44032  \u48156 \u49373 \u54664 \u49845 \u45768 \u45796 : \cf0 \strokec4 \{e\}\cf6 \strokec6 "\cf0 \strokec4 )\cb1 \
\cb3         st.stop()\cb1 \
\
\cb3     \cf5 \strokec5 # 2. \uc0\u47784 \u45944  \u48143  \u49464 \u49496  \u52488 \u44592 \u54868 \cf0 \cb1 \strokec4 \
\cb3     \cf2 \strokec2 try\cf0 \strokec4 :\cb1 \
\cb3         model = genai.GenerativeModel(\cb1 \
\cb3             model_name=\cf6 \strokec6 "gemini-1.5-flash-latest"\cf0 \strokec4 ,\cb1 \
\cb3             system_instruction=SYSTEM_PROMPT\cb1 \
\cb3         )\cb1 \
\cb3         initialize_session(model)\cb1 \
\cb3     \cf2 \strokec2 except\cf0 \strokec4  Exception \cf2 \strokec2 as\cf0 \strokec4  e:\cb1 \
\cb3         st.error(\cf6 \strokec6 f"\uc0\u47784 \u45944  \u47196 \u46377  \u51473  \u50724 \u47448 \u44032  \u48156 \u49373 \u54664 \u49845 \u45768 \u45796 : \cf0 \strokec4 \{e\}\cf6 \strokec6 "\cf0 \strokec4 )\cb1 \
\cb3         st.stop()\cb1 \
\
\cb3     \cf5 \strokec5 # 3. \uc0\u49324 \u51060 \u46300 \u48148  (\u49444 \u51221  \u48143  \u51228 \u50612 )\cf0 \cb1 \strokec4 \
\cb3     \cf2 \strokec2 with\cf0 \strokec4  st.sidebar:\cb1 \
\cb3         st.title(\cf6 \strokec6 "\uc0\u52311 \u48391  \u51228 \u50612 \u54032 "\cf0 \strokec4 )\cb1 \
\cb3         \cb1 \
\cb3         \cf5 \strokec5 # \uc0\u45824 \u54868  \u52488 \u44592 \u54868 \cf0 \cb1 \strokec4 \
\cb3         \cf2 \strokec2 if\cf0 \strokec4  st.button(\cf6 \strokec6 "\uc0\u45824 \u54868  \u52488 \u44592 \u54868 "\cf0 \strokec4 , key=\cf6 \strokec6 "reset_chat"\cf0 \strokec4 ):\cb1 \
\cb3             \cf5 \strokec5 # \uc0\u49464 \u49496  \u49345 \u53468 \u51032  \u51452 \u50836  \u54637 \u47785 \u51012  \u52488 \u44592 \u54868 \cf0 \cb1 \strokec4 \
\cb3             st.session_state.chat_session = model.start_chat(history=[])\cb1 \
\cb3             st.session_state.messages = [\cb1 \
\cb3                 \{\cf6 \strokec6 "role"\cf0 \strokec4 : \cf6 \strokec6 "model"\cf0 \strokec4 , \cf6 \strokec6 "parts"\cf0 \strokec4 : [\cf6 \strokec6 "\uc0\u45824 \u54868 \u44032  \u52488 \u44592 \u54868 \u46104 \u50632 \u49845 \u45768 \u45796 . \u47924 \u50631 \u51060  \u44417 \u44552 \u54616 \u49888 \u44032 \u50836 ?"\cf0 \strokec4 ]\}\cb1 \
\cb3             ]\cb1 \
\cb3             \cf5 \strokec5 # \uc0\u47196 \u44536 \u45716  \u50976 \u51648 \u54616 \u46104 , \u49352  \u49464 \u49496  ID\u47196  \u44396 \u48516 \cf0 \cb1 \strokec4 \
\cb3             st.session_state.session_id = \cf6 \strokec6 f"session_\cf0 \strokec4 \{datetime.now().strftime('%Y%m%d_%H%M%S')\}\cf6 \strokec6 "\cf0 \cb1 \strokec4 \
\cb3             st.rerun()\cb1 \
\
\cb3         st.divider()\cb1 \
\
\cb3         \cf5 \strokec5 # \uc0\u47196 \u44536  \u44592 \u47197  \u49444 \u51221 \cf0 \cb1 \strokec4 \
\cb3         log_enabled = st.checkbox(\cf6 \strokec6 "\uc0\u45824 \u54868  \u51088 \u46041  \u44592 \u47197  (CSV\u50857 )"\cf0 \strokec4 , value=\cf2 \strokec2 True\cf0 \strokec4 , key=\cf6 \strokec6 "log_toggle"\cf0 \strokec4 )\cb1 \
\
\cb3         \cf5 \strokec5 # \uc0\u47196 \u44536  \u45796 \u50868 \u47196 \u46300 \cf0 \cb1 \strokec4 \
\cb3         \cf2 \strokec2 if\cf0 \strokec4  st.session_state.log:\cb1 \
\cb3             \cf2 \strokec2 try\cf0 \strokec4 :\cb1 \
\cb3                 df = pd.DataFrame(st.session_state.log)\cb1 \
\cb3                 \cf5 \strokec5 # UTF-8-SIG\uc0\u47196  \u51064 \u53076 \u46377 \u54616 \u50668  Excel\u50640 \u49436  \u54620 \u44544  \u44648 \u51664  \u48169 \u51648 \cf0 \cb1 \strokec4 \
\cb3                 csv_data = df.to_csv(index=\cf2 \strokec2 False\cf0 \strokec4 , encoding=\cf6 \strokec6 'utf-8-sig'\cf0 \strokec4 )\cb1 \
\cb3                 st.download_button(\cb1 \
\cb3                     label=\cf6 \strokec6 "\uc0\u45824 \u54868  \u47196 \u44536  \u45796 \u50868 \u47196 \u46300  (.csv)"\cf0 \strokec4 ,\cb1 \
\cb3                     data=csv_data,\cb1 \
\cb3                     file_name=\cf6 \strokec6 f"chat_log_\cf0 \strokec4 \{st.session_state.session_id\}\cf6 \strokec6 .csv"\cf0 \strokec4 ,\cb1 \
\cb3                     mime=\cf6 \strokec6 "text/csv"\cf0 \strokec4 ,\cb1 \
\cb3                 )\cb1 \
\cb3             \cf2 \strokec2 except\cf0 \strokec4  Exception \cf2 \strokec2 as\cf0 \strokec4  e:\cb1 \
\cb3                 st.error(\cf6 \strokec6 f"\uc0\u47196 \u44536  \u54028 \u51068  \u49373 \u49457  \u51473  \u50724 \u47448 : \cf0 \strokec4 \{e\}\cf6 \strokec6 "\cf0 \strokec4 )\cb1 \
\cb3         \cb1 \
\cb3         st.divider()\cb1 \
\cb3         \cb1 \
\cb3         \cf5 \strokec5 # \uc0\u47784 \u45944  \u48143  \u49464 \u49496  \u51221 \u48372  \u54364 \u49884 \cf0 \cb1 \strokec4 \
\cb3         st.info(\cf6 \strokec6 f"**Model:** gemini-1.5-flash-latest\\n\\n"\cf0 \cb1 \strokec4 \
\cb3                 \cf6 \strokec6 f"**Session:** \cf0 \strokec4 \{st.session_state.session_id\}\cf6 \strokec6 "\cf0 \strokec4 )\cb1 \
\
\cb3     \cf5 \strokec5 # 4. \uc0\u47700 \u51064  \u52311  \u51064 \u53552 \u54168 \u51060 \u49828 \cf0 \cb1 \strokec4 \
\cb3     st.title(\cf6 \strokec6 "\uc0\u48120 \u46356 \u50612 \u52964 \u48036 \u45768 \u52992 \u51060 \u49496 \u54617 \u44284  Q&A \u52311 \u48391  \u55356 \u57235 "\cf0 \strokec4 )\cb1 \
\cb3     st.caption(\cf6 \strokec6 "\uc0\u50668 \u47084 \u48516 \u51032  \u46304 \u46304 \u54620  \u54617 \u44284  \u49440 \u48176 /\u51312 \u44368 \u44032  \u46104 \u50612 \u51460  AI \u52311 \u48391 \u51077 \u45768 \u45796 ."\cf0 \strokec4 )\cb1 \
\
\cb3     \cf5 \strokec5 # 4-1. \uc0\u51060 \u51204  \u45824 \u54868  \u45236 \u50669  \u54364 \u49884 \cf0 \cb1 \strokec4 \
\cb3     \cf2 \strokec2 for\cf0 \strokec4  message \cf2 \strokec2 in\cf0 \strokec4  st.session_state.messages:\cb1 \
\cb3         role = \cf6 \strokec6 "assistant"\cf0 \strokec4  \cf2 \strokec2 if\cf0 \strokec4  message[\cf6 \strokec6 "role"\cf0 \strokec4 ] == \cf6 \strokec6 "model"\cf0 \strokec4  \cf2 \strokec2 else\cf0 \strokec4  \cf6 \strokec6 "user"\cf0 \cb1 \strokec4 \
\cb3         \cf2 \strokec2 with\cf0 \strokec4  st.chat_message(role):\cb1 \
\cb3             st.markdown(message[\cf6 \strokec6 "parts"\cf0 \strokec4 ][\cf7 \strokec7 0\cf0 \strokec4 ])\cb1 \
\
\cb3     \cf5 \strokec5 # 4-2. \uc0\u49324 \u50857 \u51088  \u51077 \u47141  \u52376 \u47532 \cf0 \cb1 \strokec4 \
\cb3     \cf2 \strokec2 if\cf0 \strokec4  prompt := st.chat_input(\cf6 \strokec6 "\uc0\u51320 \u50629  \u50836 \u44148 , \u51109 \u54617 \u44552  \u46321  \u44417 \u44552 \u54620  \u51216 \u51012  \u47932 \u50612 \u48372 \u49464 \u50836 ."\cf0 \strokec4 ):\cb1 \
\cb3         \cf5 \strokec5 # \uc0\u49324 \u50857 \u51088  \u47700 \u49884 \u51648  \u54364 \u49884  \u48143  \u44592 \u47197 \cf0 \cb1 \strokec4 \
\cb3         st.chat_message(\cf6 \strokec6 "user"\cf0 \strokec4 ).markdown(prompt)\cb1 \
\cb3         st.session_state.messages.append(\{\cf6 \strokec6 "role"\cf0 \strokec4 : \cf6 \strokec6 "user"\cf0 \strokec4 , \cf6 \strokec6 "parts"\cf0 \strokec4 : [prompt]\})\cb1 \
\cb3         log_message(\cf6 \strokec6 "user"\cf0 \strokec4 , prompt, log_enabled)\cb1 \
\
\cb3         \cf5 \strokec5 # 4-3. API \uc0\u52968 \u53581 \u49828 \u53944  \u44288 \u47532  (\u50836 \u52397 : \u52572 \u44540  6\u53556 )\cf0 \cb1 \strokec4 \
\cb3         \cf5 \strokec5 # Gemini ChatSession\uc0\u51008  \u45236 \u48512 \u51201 \u51004 \u47196  \u55176 \u49828 \u53664 \u47532 \u47484  \u44288 \u47532 \u54633 \u45768 \u45796 .\cf0 \cb1 \strokec4 \
\cb3         \cf5 \strokec5 # \uc0\u47564 \u50557  6\u53556 (user 3, model 3)\u51012  \u52488 \u44284 \u54616 \u47732 , \u49464 \u49496 \u51012  \u47560 \u51648 \u47561  6\u44060  \u47700 \u49884 \u51648 \u47196  \u51116 \u49884 \u51089 \u54633 \u45768 \u45796 .\cf0 \cb1 \strokec4 \
\cb3         \cf5 \strokec5 # (\uc0\u52280 \u44256 : messages \u47532 \u49828 \u53944 \u50640 \u45716  \u52488 \u44592  \u51064 \u49324 \u47568 \u51060  \u54252 \u54632 \u46112  \u49688  \u51080 \u51004 \u48064 \u47196  chat_session.history\u47484  \u44592 \u51456 )\cf0 \cb1 \strokec4 \
\cb3         \cf2 \strokec2 if\cf0 \strokec4  \cf2 \strokec2 len\cf0 \strokec4 (st.session_state.chat_session.history) > \cf7 \strokec7 6\cf0 \strokec4 :\cb1 \
\cb3             \cf2 \strokec2 try\cf0 \strokec4 :\cb1 \
\cb3                 \cf5 \strokec5 # \uc0\u47560 \u51648 \u47561  6\u44060  \u53556 \u51004 \u47196  \u55176 \u49828 \u53664 \u47532  \u52629 \u49548 \u54616 \u50668  \u49464 \u49496  \u51116 \u49884 \u51089 \cf0 \cb1 \strokec4 \
\cb3                 st.session_state.chat_session = model.start_chat(\cb1 \
\cb3                     history=st.session_state.chat_session.history[\cf7 \strokec7 -6\cf0 \strokec4 :]\cb1 \
\cb3                 )\cb1 \
\cb3                 \cf2 \strokec2 print\cf0 \strokec4 (\cf6 \strokec6 f"Context truncated. History length: \cf0 \strokec4 \{len(st.session_state.chat_session.history)\}\cf6 \strokec6 "\cf0 \strokec4 )\cb1 \
\cb3             \cf2 \strokec2 except\cf0 \strokec4  Exception \cf2 \strokec2 as\cf0 \strokec4  e:\cb1 \
\cb3                 st.warning(\cf6 \strokec6 f"\uc0\u55176 \u49828 \u53664 \u47532  \u51116 \u49884 \u51089  \u51473  \u50724 \u47448 : \cf0 \strokec4 \{e\}\cf6 \strokec6 "\cf0 \strokec4 )\cb1 \
\
\cb3         \cf5 \strokec5 # 4-4. Gemini API \uc0\u54840 \u52636 \cf0 \cb1 \strokec4 \
\cb3         \cf2 \strokec2 try\cf0 \strokec4 :\cb1 \
\cb3             \cf2 \strokec2 with\cf0 \strokec4  st.chat_message(\cf6 \strokec6 "assistant"\cf0 \strokec4 ):\cb1 \
\cb3                 \cf2 \strokec2 with\cf0 \strokec4  st.spinner(\cf6 \strokec6 "\uc0\u45813 \u48320 \u51012  \u49373 \u44033  \u51473 \u51060 \u50640 \u50836 ..."\cf0 \strokec4 ):\cb1 \
\cb3                     \cf5 \strokec5 # ChatSession\uc0\u51012  \u53685 \u54644  \u47700 \u49884 \u51648  \u51204 \u49569 \cf0 \cb1 \strokec4 \
\cb3                     response = st.session_state.chat_session.send_message(prompt)\cb1 \
\cb3                     response_text = response.text\cb1 \
\cb3             \cb1 \
\cb3             \cf5 \strokec5 # \uc0\u47784 \u45944  \u51025 \u45813  \u54364 \u49884  \u48143  \u44592 \u47197 \cf0 \cb1 \strokec4 \
\cb3             st.session_state.messages.append(\{\cf6 \strokec6 "role"\cf0 \strokec4 : \cf6 \strokec6 "model"\cf0 \strokec4 , \cf6 \strokec6 "parts"\cf0 \strokec4 : [response_text]\})\cb1 \
\cb3             log_message(\cf6 \strokec6 "model"\cf0 \strokec4 , response_text, log_enabled)\cb1 \
\cb3             \cb1 \
\cb3             \cf5 \strokec5 # \uc0\u54868 \u47732 \u51012  \u51593 \u49884  \u49352 \u47196 \u44256 \u52840 \u54616 \u50668  \u47784 \u45944 \u51032  \u47560 \u51648 \u47561  \u45813 \u48320 \u51012  \u54364 \u49884 \cf0 \cb1 \strokec4 \
\cb3             st.rerun()\cb1 \
\
\cb3         \cf2 \strokec2 except\cf0 \strokec4  genai.types.StopCandidateException \cf2 \strokec2 as\cf0 \strokec4  e:\cb1 \
\cb3             st.error(\cf6 \strokec6 f"\uc0\u45813 \u48320  \u49373 \u49457  \u51473 \u51648 \u46120 : \cf0 \strokec4 \{e\}\cf6 \strokec6 "\cf0 \strokec4 )\cb1 \
\cb3             log_message(\cf6 \strokec6 "system_error"\cf0 \strokec4 , \cf6 \strokec6 f"StopCandidateException: \cf0 \strokec4 \{e\}\cf6 \strokec6 "\cf0 \strokec4 , log_enabled)\cb1 \
\cb3         \cf2 \strokec2 except\cf0 \strokec4  genai.types.BrokenResponseError \cf2 \strokec2 as\cf0 \strokec4  e:\cb1 \
\cb3             st.error(\cf6 \strokec6 f"API \uc0\u51025 \u45813  \u50724 \u47448 : \cf0 \strokec4 \{e\}\cf6 \strokec6 "\cf0 \strokec4 )\cb1 \
\cb3             log_message(\cf6 \strokec6 "system_error"\cf0 \strokec4 , \cf6 \strokec6 f"BrokenResponseError: \cf0 \strokec4 \{e\}\cf6 \strokec6 "\cf0 \strokec4 , log_enabled)\cb1 \
\cb3         \cf2 \strokec2 except\cf0 \strokec4  Exception \cf2 \strokec2 as\cf0 \strokec4  e:\cb1 \
\cb3             \cf5 \strokec5 # 429 (Resource Exhausted) \uc0\u50640 \u47084  \u46321  \u51068 \u48152 \u51201 \u51064  API \u50696 \u50808  \u52376 \u47532 \cf0 \cb1 \strokec4 \
\cb3             st.error(\cf6 \strokec6 f"\uc0\u47700 \u49884 \u51648  \u51204 \u49569  \u51473  \u50724 \u47448 \u44032  \u48156 \u49373 \u54664 \u49845 \u45768 \u45796 : \cf0 \strokec4 \{e\}\cf6 \strokec6 "\cf0 \strokec4 )\cb1 \
\cb3             log_message(\cf6 \strokec6 "system_error"\cf0 \strokec4 , \cf6 \strokec6 f"Exception: \cf0 \strokec4 \{e\}\cf6 \strokec6 "\cf0 \strokec4 , log_enabled)\cb1 \
\cb3             \cf5 \strokec5 # 429 \uc0\u50640 \u47084 \u51032  \u44221 \u50864 , Streamlit\u51060  \u51088 \u46041 \u51004 \u47196  \u51116 \u49884 \u46020 \u54616 \u51648  \u50506 \u51004 \u48064 \u47196  \cf0 \cb1 \strokec4 \
\cb3             \cf5 \strokec5 # \uc0\u49324 \u50857 \u51088 \u50640 \u44172  \u51104 \u49884  \u54980  \u45796 \u49884  \u49884 \u46020 \u54616 \u46972 \u44256  \u50504 \u45236 \u54616 \u45716  \u44163 \u51060  \u51339 \u49845 \u45768 \u45796 .\cf0 \cb1 \strokec4 \
\cb3             \cf2 \strokec2 if\cf0 \strokec4  \cf6 \strokec6 "429"\cf0 \strokec4  \cf2 \strokec2 in\cf0 \strokec4  \cf2 \strokec2 str\cf0 \strokec4 (e):\cb1 \
\cb3                 st.warning(\cf6 \strokec6 "\uc0\u50836 \u52397 \u51060  \u45320 \u47924  \u47566 \u49845 \u45768 \u45796 . \u51104 \u49884  \u54980  \u45796 \u49884  \u49884 \u46020 \u54644 \u51452 \u49464 \u50836 ."\cf0 \strokec4 )\cb1 \
\
\
\pard\pardeftab720\partightenfactor0
\cf5 \cb3 \strokec5 # --- \uc0\u49828 \u53356 \u47549 \u53944  \u49892 \u54665  ---\cf0 \cb1 \strokec4 \
\pard\pardeftab720\partightenfactor0
\cf2 \cb3 \strokec2 if\cf0 \strokec4  \cf2 \strokec2 __name__\cf0 \strokec4  == \cf6 \strokec6 "__main__"\cf0 \strokec4 :\cb1 \
\pard\pardeftab720\partightenfactor0
\cf0 \cb3     main()\cb1 \
}
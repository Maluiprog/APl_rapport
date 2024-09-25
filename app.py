import streamlit as st
import boto3
import datetime

# Skapa en DynamoDB-resurs utan att ange nycklar
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table("inlagg")

today = datetime.datetime.today()
week_num = today.isocalendar()[1]
formatted_datetime = today.strftime("%Y-%m-%d %H:%M")

def add_entry(title, content, mood, tags, week_num, formatted_datetime):
    table.put_item(
        Item={
            'title': title,
            'content': content,
            'mood': mood,
            'tags': tags,
            'week': week_num,
            'timestamp': formatted_datetime
        }
    )

def sidebarstart():
    st.sidebar.title('Inlägg')
    st.sidebar.subheader('Lägg till inlägg')
    st.sidebar.write('Fyll i formuläret nedan för att lägga till ett nytt inlägg')
    with st.sidebar:
        title = st.text_input('Titel')
        content = st.text_area('Innehåll')
        mood = st.selectbox('Humör', ["😀", "😭", '😠', '😕', '😐'])
        tags = st.multiselect('Taggar', ['IT', 'Nätverk', 'Datorer ', 'Programmering', 'Säkerhet'])
        if st.button('Lägg till'):
            if not title or not content:
                st.error('Titel och innehåll är obligatoriska')
            else:
                add_entry(title, content, mood, tags, week_num, formatted_datetime)
                st.success('Inlägg tillagt!')

def huvudsida():
    st.title('APL-veckorapport')
    st.subheader('Inlägg')
    response = table.scan()
    items = response['Items']
    for item in items:
        st.write(f"**Vecka:** {item['week']}")
        st.write(f"**Datum:** {item['timestamp']}")
        st.write(f"**Titel:** {item['title']}")
        st.write(f"**Innehåll:** {item['content']}")
        st.write(f"**Humör:** {item['mood']}")
        st.write(f"**Taggar:** {', '.join(item['tags'])}")
        st.write('---')

sidebarstart()
huvudsida()

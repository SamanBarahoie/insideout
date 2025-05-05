import pandas as pd
import numpy as np
import plotly.express as px
import matplotlib.pyplot as plt
import streamlit as st

class MovieEmotionDashboard:
    def __init__(self, emotion_data_path, time_data_path):
        self.emotion_data_path = emotion_data_path
        self.time_data_path = time_data_path
        self.df = pd.read_csv(self.emotion_data_path)
        self.df_time = pd.read_csv(self.time_data_path)
    
    def plot_emotion_distribution(self):
        # محاسبه فراوانی هر احساس
        emotion_counts = self.df['emotion'].value_counts().reset_index()
        emotion_counts.columns = ['emotion', 'count']
        emotion_counts = emotion_counts.sort_values('count', ascending=False)

        # رسم radar chart با استایل بهتر
        fig = px.line_polar(
            emotion_counts,
            r='count',
            theta='emotion',
            line_close=True,
            title='🎬 Emotion Distribution in Movie (Radar Chart)',
            markers=True,
            color_discrete_sequence=px.colors.sequential.Plasma_r
        )

        # نمایش مقدار روی هر نقطه
        fig.update_traces(
            fill='toself',
            text=emotion_counts['count'],
            textposition='top center'
        )

        # بهبود layout
        fig.update_layout(
            polar=dict(
                radialaxis=dict(showticklabels=True, ticks='outside', tickfont_size=12),
                angularaxis=dict(tickfont_size=12)
            ),
            title_font_size=20
        )

        # نمایش در Streamlit
        st.plotly_chart(fig)
    
    def plot_fear_over_time(self):
        # تقسیم تایم‌لاین به ۱۰ بخش مساوی
        t_min, t_max = self.df_time['time'].min(), self.df_time['time'].max()
        bins = np.linspace(t_min, t_max, 11)
        self.df_time['segment'] = pd.cut(self.df_time['time'], bins=bins, labels=False, include_lowest=True)

        # محاسبه تعداد خطوط 'fear' در هر بخش
        fear_counts = self.df_time[self.df_time['emotion'] == 'fear'].groupby('segment').size().reindex(range(10), fill_value=0)

        # محاسبه زمان میانه هر بخش
        mid_times = (bins[:-1] + bins[1:]) / 2

        # تبدیل زمان به فرمت MM:SS
        def sec_to_mmss(x):
            m = int(x // 60)
            s = int(x % 60)
            return f"{m:02d}:{s:02d}"

        x_labels = [sec_to_mmss(t) for t in mid_times]

        # رسم خطی با Matplotlib
        plt.figure(figsize=(10, 5))
        plt.plot(mid_times, fear_counts.values, marker='o', linewidth=2, color='crimson')
        plt.title('Fear Level Over Movie (10 Equal Time Segments)')
        plt.xlabel('Time (MM:SS)')
        plt.ylabel('Number of Fearful Lines')
        plt.xticks(mid_times, x_labels, rotation=45)
        plt.grid(alpha=0.3)
        plt.tight_layout()

        # نمایش در Streamlit
        st.pyplot(plt)
    
    def plot_riley_joy_over_time(self):
        # فیلتر کردن داده‌ها برای "Riley" و احساس "joy"
        riley_joy_df = self.df_time[(self.df_time['line'].str.contains('Riley', case=False)) & (self.df_time['emotion'] == 'joy')]

        # تقسیم تایم‌لاین به ۱۰ بخش مساوی
        t_min, t_max = riley_joy_df['time'].min(), riley_joy_df['time'].max()
        bins = np.linspace(t_min, t_max, 11)
        riley_joy_df['segment'] = pd.cut(riley_joy_df['time'], bins=bins, labels=False, include_lowest=True)

        # محاسبه تعداد خطوط 'joy' در هر بخش
        joy_counts = riley_joy_df.groupby('segment').size().reindex(range(10), fill_value=0)

        # محاسبه زمان میانه هر بخش
        mid_times = (bins[:-1] + bins[1:]) / 2

        # تبدیل زمان به فرمت MM:SS
        def sec_to_mmss(x):
            m = int(x // 60)
            s = int(x % 60)
            return f"{m:02d}:{s:02d}"

        x_labels = [sec_to_mmss(t) for t in mid_times]

        # رسم خطی با Matplotlib
        plt.figure(figsize=(10, 5))
        plt.plot(mid_times, joy_counts.values, marker='o', linewidth=2, color='yellowgreen')
        plt.title('Riley Joy Level Over Movie (10 Equal Time Segments)')
        plt.xlabel('Time (MM:SS)')
        plt.ylabel('Number of Joyful Lines with Riley')
        plt.xticks(mid_times, x_labels, rotation=45)
        plt.grid(alpha=0.3)
        plt.tight_layout()

        # نمایش در Streamlit
        st.pyplot(plt)

    def plot_average_emotion_score(self):
        # محاسبه میانگین امتیاز احساسات برای Riley
        mean_scores = self.df.groupby('emotion')['score'].mean().reset_index()

        # رسم bar chart با Plotly
        fig = px.bar(mean_scores, x='emotion', y='score',
                     title='Average Emotion Score for Riley',
                     labels={'score': 'Average Score'})
        st.plotly_chart(fig)

    def plot_emotion_pie_chart(self):
        # محاسبه فراوانی هر احساس برای نمودار دایره‌ای
        emotion_counts = self.df['emotion'].value_counts().reset_index()
        emotion_counts.columns = ['emotion', 'count']

        # رسم Pie Chart با Plotly
        fig = px.pie(emotion_counts, names='emotion', values='count', title='Emotion Distribution Pie Chart')
        
        # نمایش در Streamlit
        st.plotly_chart(fig)


# ساخت شی از کلاس MovieEmotionDashboard
dashboard = MovieEmotionDashboard(emotion_data_path='emotion_results_with_time.csv', time_data_path='emotion_results_with_time.csv')

# تنظیمات Streamlit
st.title('🎬 Movie Emotion Dashboard')

# نمایش نمودارهای مختلف
dashboard.plot_emotion_pie_chart()
dashboard.plot_emotion_distribution()
dashboard.plot_fear_over_time()
dashboard.plot_riley_joy_over_time()
dashboard.plot_average_emotion_score()

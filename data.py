import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
import re
from wordcloud import WordCloud

class TweetAnalyzer:
    def __init__(self, file_path='tweets.csv'):
        """
        Inisialisasi TweetAnalyzer
        
        Parameters:
        file_path (str): Path ke file CSV yang berisi data tweets
        """
        self.file_path = file_path
        self.df = None
        self.load_data()
        # Set style untuk visualisasi
        sns.set_style("whitegrid")
        
    def load_data(self):
        """Memuat dan membersihkan data dari file CSV"""
        try:
            self.df = pd.read_csv(self.file_path)
            # Konversi kolom waktu ke datetime
            self.df['waktu'] = pd.to_datetime(self.df['waktu'], format='%d-%m-%Y %H:%M')
            print(f"Data berhasil dimuat. Total {len(self.df)} tweets.")
        except Exception as e:
            print(f"Error saat memuat data: {str(e)}")
    
    def info_dasar(self):
        """Menampilkan informasi dasar dari dataset"""
        if self.df is not None:
            print("\nInformasi Dataset:")
            print("="*50)
            print(self.df.info())
            print("\nStatistik Deskriptif:")
            print("="*50)
            print(self.df.describe())
            
            print("\nInformasi Tambahan:")
            print("="*50)
            print(f"Periode Data: {self.df['waktu'].min()} sampai {self.df['waktu'].max()}")
            print(f"Jumlah User Unik: {self.df['username'].nunique()}")
    
    def analisis_waktu(self):
        """Analisis pola waktu posting tweets"""
        if self.df is not None:
            (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10))
            
            # Plot 1: Tweets per jam
            self.df['hour'] = self.df['waktu'].dt.hour
            hourly_tweets = self.df['hour'].value_counts().sort_index()
            sns.barplot(x=hourly_tweets.index, y=hourly_tweets.values, ax=ax1, color='skyblue')
            ax1.set_title('Distribusi Tweet Berdasarkan Jam', pad=20)
            ax1.set_xlabel('Jam')
            ax1.set_ylabel('Jumlah Tweet')
            
            # Plot 2: Tweets per hari
            daily_tweets = self.df.groupby(self.df['waktu'].dt.date).size()
            daily_tweets.plot(kind='line', ax=ax2, color='darkblue', marker='o')
            ax2.set_title('Tren Tweet per Hari', pad=20)
            ax2.set_xlabel('Tanggal')
            ax2.set_ylabel('Jumlah Tweet')
            ax2.grid(True)
            
            plt.tight_layout()
            plt.show()
    
    def analisis_user(self):
        """Analisis aktivitas user"""
        if self.df is not None:
            # Top 10 user paling aktif
            top_users = self.df['username'].value_counts().head(10)
            
            plt.figure(figsize=(12, 6))
            colors = sns.color_palette("husl", 10)
            bars = plt.barh(top_users.index, top_users.values, color=colors)
            plt.title('10 User Paling Aktif', pad=20)
            plt.xlabel('Jumlah Tweet')
            
            # Menambahkan nilai di setiap bar
            for i, bar in enumerate(bars):
                width = bar.get_width()
                plt.text(width, bar.get_y() + bar.get_height()/2,
                        f'{int(width)}',
                        ha='left', va='center', fontweight='bold')
            
            plt.tight_layout()
            plt.show()
    
    def analisis_konten(self):
        """Analisis konten tweet"""
        if self.df is not None:
            # Gabungkan semua teks
            text = ' '.join(self.df['konten'].astype(str))
            
            #  word cloud
            wordcloud = WordCloud(
                width=800, 
                height=400,
                background_color='white',
                max_words=100,
                colormap='viridis'
            ).generate(text)
            
            plt.figure(figsize=(15, 8))
            plt.imshow(wordcloud, interpolation='bilinear')
            plt.axis('off')
            plt.title('Word Cloud dari Konten Tweet', pad=20)
            plt.show()
            
            # Analisis panjang tweet
            self.df['tweet_length'] = self.df['konten'].str.len()
            
            plt.figure(figsize=(10, 6))
            sns.histplot(data=self.df, x='tweet_length', bins=30, color='purple', alpha=0.6)
            plt.title('Distribusi Panjang Tweet', pad=20)
            plt.xlabel('Panjang Tweet (Karakter)')
            plt.ylabel('Frekuensi')
            
            # statistik ke plot
            avg_len = self.df['tweet_length'].mean()
            median_len = self.df['tweet_length'].median()
            plt.axvline(x=avg_len, color='red', linestyle='--', label=f'Rata-rata: {int(avg_len)}')
            plt.axvline(x=median_len, color='green', linestyle='--', label=f'Median: {int(median_len)}')
            plt.legend()
            
            plt.tight_layout()
            plt.show()
    
    def export_data(self, output_dir='hasil_analisis'):
        """
        Export data ke format CSV dan Excel dengan analisis tambahan
        
        Parameters:
        output_dir (str): Direktori untuk menyimpan hasil
        """
        if self.df is not None:
            try:
                if not os.path.exists(output_dir):
                    os.makedirs(output_dir)
                
                # Tambah kolom analisis
                df_export = self.df.copy()
                df_export['waktu_post'] = df_export['waktu'].dt.strftime('%Y-%m-%d %H:%M:%S')
                df_export['hari'] = df_export['waktu'].dt.day_name()
                df_export['jam'] = df_export['waktu'].dt.hour
                df_export['panjang_tweet'] = df_export['konten'].str.len()
                
                # Export ke CSV
                csv_path = f'{output_dir}/data_tweets_analyzed.csv'
                df_export.to_csv(csv_path, index=False)
                print(f"Data berhasil disimpan ke {csv_path}")
                
                # Export ke Excel dengan format yang lebih baik
                excel_path = f'{output_dir}/data_tweets_analyzed.xlsx'
                
                with pd.ExcelWriter(excel_path, engine='xlsxwriter') as writer:
                    # Sheet 1: Data utama
                    df_export.to_excel(writer, sheet_name='Data Tweets', index=False)
                    
                    # Sheet 2: Analisis per user
                    user_stats = pd.DataFrame({
                        'total_tweets': df_export['username'].value_counts(),
                    })
                    user_stats['rata_panjang_tweet'] = df_export.groupby('username')['panjang_tweet'].mean().round(2)
                    user_stats.to_excel(writer, sheet_name='Analisis User')
                    
                    # Sheet 3: Analisis waktu
                    tweets_per_jam = df_export['jam'].value_counts().sort_index()
                    
                    time_stats = pd.DataFrame({
                        'jam': tweets_per_jam.index,
                        'tweets_per_jam': tweets_per_jam.values,
                    })
                    time_stats.to_excel(writer, sheet_name='Analisis Waktu', index=False)
                    
                    # Format
                    workbook = writer.book
                    for worksheet in writer.sheets.values():
                        worksheet.set_column('A:Z', 15)  # Set lebar kolom
                        
                        # Format header
                        header_format = workbook.add_format({
                            'bold': True,
                            'align': 'center',
                            'bg_color': '#D3D3D3',
                            'border': 1
                        })
                        
                        # Aplikasikan format ke header
                        for col_num, value in enumerate(df_export.columns.values):
                            worksheet.write(0, col_num, value, header_format)
                
                print(f"Data berhasil disimpan ke {excel_path}")
                return True
                
            except Exception as e:
                print(f"Error saat export data: {str(e)}")
                return False
        return False

    def analisis_sentimen(self):
        """Menganalisis distribusi sentimen jika kolom sentiment ada"""
        if 'sentiment' in self.df.columns:
            sentiment_counts = self.df['sentiment'].value_counts()
            plt.figure(figsize=(10, 6))
            sns.barplot(x=sentiment_counts.index, y=sentiment_counts.values)
            plt.title('Distribusi Sentimen Tweet')
            plt.xlabel('Sentimen')
            plt.ylabel('Jumlah Tweet')
            plt.show()
    
    def top_hashtags(self, n=10):
        """
        Menampilkan top N hashtags
        
        Parameters:
        n (int): Jumlah top hashtags yang ingin ditampilkan
        """
        if 'text' in self.df.columns:
            hashtags = []
            for text in self.df['text']:
                if isinstance(text, str):
                    tags = [tag.strip('#') for tag in text.split() if tag.startswith('#')]
                    hashtags.extend(tags)
            
            hashtag_counts = pd.Series(hashtags).value_counts().head(n)
            plt.figure(figsize=(12, 6))
            sns.barplot(x=hashtag_counts.values, y=hashtag_counts.index)
            plt.title(f'Top {n} Hashtags')
            plt.xlabel('Jumlah Penggunaan')
            plt.ylabel('Hashtag')
            plt.show()

class TweetCleaner:
    @staticmethod
    def clean_text(text):
        if not isinstance(text, str):
            return ""
            
        # Hapus pengulangan angka
        text = re.sub(r'(\d+)(\s+\1)+', r'\1', text)
        
        # Hapus "Show more" dan teks setelahnya
        text = re.sub(r'Show more.*$', '', text)
        
        # Hapus URL
        text = re.sub(r'https?://\S+', '', text)
        
        # Hapus mention berulang
        text = re.sub(r'(@\w+\s*){2,}', r'\1', text)
        
        # Hapus pengulangan nama di awal
        text = re.sub(r'([A-Za-z]+)\s+\1\s+@\w+\s+·\s+', '', text)
        
        # Bersihkan spasi
        text = ' '.join(text.split())
        return text.strip()

    @staticmethod
    def clean_username(username):
        if not isinstance(username, str):
            return ""
            
        # Hapus pengulangan dan format username
        username = re.sub(r'([A-Za-z0-9_]+)(?:\s+\1)*(?:\s+@\w+)*', r'\1', username)
        return username.strip()

def process_tweets():
    try:
        # Baca file CSV
        df = pd.read_csv('tweets.csv')
        
        # Buat instance TweetCleaner
        cleaner = TweetCleaner()
        
        # Bersihkan data
        df['konten'] = df['konten'].apply(cleaner.clean_text)
        df['username'] = df['username'].apply(cleaner.clean_username)
        
        # Hapus tweet kosong
        df = df[df['konten'].str.len() > 0]
        
        # Hitung panjang tweet
        df['tweet_length'] = df['konten'].str.len()
        
        # Urutkan berdasarkan waktu
        df['waktu'] = pd.to_datetime(df['waktu'], format='%d-%m-%Y %H:%M')
        df = df.sort_values('waktu', ascending=False)
        
        # Simpan hasil ke CSV
        df.to_csv('tweets_clean.csv', index=False)
        print(f"Data berhasil dibersihkan dan disimpan ke tweets_clean.csv")
        
        # Tampilkan statistik
        print("\nStatistik Data:")
        print(f"Total tweets: {len(df)}")
        print(f"User unik: {df['username'].nunique()}")
        print(f"Rata-rata panjang tweet: {df['tweet_length'].mean():.0f} karakter")
        
        
        print("\nSemua Tweet (Diurutkan dari Terbaru):")
        print("=" * 100)
        for idx, row in df.iterrows():
            print(f"\n[{idx + 1}] User: {row['username']}")
            print(f"Waktu: {row['waktu'].strftime('%d-%m-%Y %H:%M')}")
            print(f"Tweet: {row['konten']}")
            print("-" * 100)
        
    except Exception as e:
        print(f"Error saat memproses data: {str(e)}")

def main():
    """Fungsi utama untuk menjalankan analisis"""
    analyzer = TweetAnalyzer()
    
    
    analyzer.info_dasar()
    
   
    print("\nMenganalisis pola waktu posting...")
    analyzer.analisis_waktu()
    
    
    print("\nMenganalisis aktivitas user...")
    analyzer.analisis_user()
    
    
    print("\nMenganalisis konten tweet...")
    analyzer.analisis_konten()
    
    # Export data
    print("\nMengexport hasil analisis...")
    analyzer.export_data()

if __name__ == "__main__":
    process_tweets()

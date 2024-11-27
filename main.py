# İçeri Aktarma
from flask import Flask, render_template,request, redirect
# Veritabanı kütüphanesini içe aktarma
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
# SQLite ile bağlantı kurma 
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///diary.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# DB oluşturma
db = SQLAlchemy(app )

#Görev #1. DB tablosu oluşturma
class Card(db.Model):
    title=db.Column(db.String(13),nullable=False)
    subtitle=db.Column(db.String(50),nullable=False)
    text=db.Column(db.String(300),nullable=False)
    id=db.Column(db.Integer,nullable=False,primary_key=True)
    def __repr__(self):
        return f'<Card {self.id}>'











# İçerik sayfasını çalıştırma
@app.route('/')
def index():
    # DB nesnelerini görüntüleme
    # Görev #2. DB'deki nesneleri index.html'de görüntüleme
    kartlar=Card.query.all()
    

    return render_template('index.html',
                           cards=kartlar

                           )

# Kartla sayfayı çalıştırma
@app.route('/card/<int:id>')
def card(id):
    # Görev #2. Id'ye göre doğru kartı görüntüleme
    card=Card.query.get(id)

    return render_template('card.html', card=card)

# Sayfayı çalıştırma ve kart oluşturma
@app.route('/create')
def create():
    return render_template('create_card.html')

# Kart formu
@app.route('/form_create', methods=['GET','POST'])
def form_create():
    if request.method == 'POST':
        title =  request.form['title']
        subtitle =  request.form['subtitle']
        metin =  request.form['text']

        # Görev #2. Verileri DB'de depolamak için bir yol oluşturma
        ege=Card(title=title,subtitle=subtitle,text=metin)
        db.session.add(ege)
        db.session.commit()



        return redirect('/')
    else:
        return render_template('create_card.html')
    
@app.route('/delete/<int:id>')
def delete(id):
    card=Card.query.get(id)
    if card:#Öğretmenim nolur nolmaz diye ekledim bunu 
        db.session.delete(card)
        db.session.commit()
    return render_template('index.html')



if __name__ == "__main__":
    with app.app_context():
         db.create_all()
    app.run(debug=True)

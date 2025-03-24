from flask import Flask, render_template, request, jsonify, url_for
from flask_sqlalchemy import SQLAlchemy
from collections import OrderedDict

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///museum.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Culture(db.Model):
    __tablename__ = 'cultures'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    region = db.Column(db.String(100))
    description = db.Column(db.Text)
    image_url = db.Column(db.String(250))
    artifacts = db.relationship('Artifact', backref='culture', lazy=True)

class Artifact(db.Model):
    __tablename__ = 'artifacts'
    id = db.Column(db.Integer, primary_key=True)
    culture_id = db.Column(db.Integer, db.ForeignKey('cultures.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    era = db.Column(db.String(50))
    description = db.Column(db.Text)
    image_url = db.Column(db.String(250))

def setup_database():
    with app.app_context():
        db.drop_all()
        db.create_all()
        if not Culture.query.first():
            seed_sample_data()

def seed_sample_data():
    asian = Culture(name="Asian Culture", region="Asia", description="A rich tapestry of traditions and art forms.", image_url="https://asiancustoms.eu/wp-content/uploads/2016/12/asianculture.jpg")
    european = Culture(name="European Culture", region="Europe", description="A blend of historical marvels and modern influence.", image_url="https://thebitetour.com/wp-content/uploads/2015/03/europe-festivals.jpg")
    african = Culture(name="African Culture", region="Africa", description="Vibrant practices and a deep sense of community.", image_url="https://i.pinimg.com/originals/2b/3d/32/2b3d32b3fb45030e54736e3c7ed3945f.jpg")
    north_american = Culture(name="North American Culture", region="North America", description="Diverse influences spanning a vast land.", image_url="https://static.vecteezy.com/system/resources/previews/026/437/358/large_2x/indigenous-women-in-traditional-clothing-showcase-north-american-tribal-culture-generated-by-ai-free-photo.jpg")
    south_american = Culture(name="South American Culture", region="South America", description="A vibrant mosaic of indigenous and modern practices.", image_url="https://images.squarespace-cdn.com/content/v1/59b9f24c64b05fd6531db026/1525638791259-Z6AA1QZNMHVFDLYIYCPI/ke17ZwdGBToddI8pDm48kCpX2mwG9slVUzQCwhOMrQF7gQa3H78H3Y0txjaiv_0fDoOvxcdMmMKkDsyUqMSsMWxHk725yiiHCCLfrh8O1z5QPOohDIaIeljMHgDF5CVlOqpeNLcJ80NK65_fV7S1UVDXM9yQ8sG6x3COIEUaadqpk9XPubC0H4MH9Az_c7nPqIjSxZ2rgD2_Fw9U6DWfsg/DSC_8427.jpg")
    oceania = Culture(name="Oceanian Culture", region="Oceania", description="Distinct island traditions and natural beauty.", image_url="https://cdn.britannica.com/66/195766-004-7175928A.jpg")
    antarctica = Culture(name="Antarctic Culture", region="Antarctica", description="Nomadic explorers and scientific research define this unique region.", image_url="https://th.bing.com/th/id/OIP.QAWhKtP7vtMNyEo5JzGFQQAAAA?rs=1&pid=ImgDetMain")
    
    artifact1 = Artifact(culture=asian, name="Ceramic Vase", era="Ming Dynasty", description="A beautifully crafted vase from ancient China.", image_url="https://d2mpxrrcad19ou.cloudfront.net/item_images/828300/10248479_fullsize.jpg")
    artifact2 = Artifact(culture=asian, name="Samurai Sword", era="Feudal Japan", description="A weapon symbolizing honor and craftsmanship.", image_url="https://th.bing.com/th/id/OIP.m-CYd8BWhL2cdwaRRmFPzwHaDa?rs=1&pid=ImgDetMain")
    
    artifact3 = Artifact(culture=european, name="Medieval Sword", era="Middle Ages", description="A sword that echoes tales of ancient battles.", image_url="https://th.bing.com/th/id/OIP.ozPbUqOnX9op2Ubpsq4CGwHaHa?w=182&h=182&c=7&r=0&o=5&dpr=1.3&pid=1.7")
    artifact4 = Artifact(culture=european, name="Roman Helmet", era="Roman Empire", description="A protective gear used by Roman soldiers.", image_url="https://as1.ftcdn.net/v2/jpg/05/59/84/28/1000_F_559842849_zc2nrVcjDDwSWboPKj2QC7yCuxbdU9cG.jpg")
    
    artifact5 = Artifact(culture=african, name="African Mask", era="18th Century", description="Traditional ceremonial mask.", image_url="https://i.pinimg.com/originals/0b/64/c7/0b64c747d1f681b400168e503cb19eac.jpg")
    artifact6 = Artifact(culture=african, name="Zulu Shield", era="19th Century", description="A shield used in traditional African warfare.", image_url="https://th.bing.com/th/id/OIP.4DTdiI-KUbajCJ-3xtbWJAAAAA?rs=1&pid=ImgDetMain")
    
    artifact7 = Artifact(culture=north_american, name="Totem Pole", era="20th Century", description="A symbolic cultural artifact.", image_url="https://thumbs.dreamstime.com/z/totem-pole-5357014.jpg")
    artifact8 = Artifact(culture=north_american, name="Cowboy Hat", era="19th Century", description="A hat symbolizing the Wild West.", image_url="https://i.etsystatic.com/14160527/r/il/f0dadd/1833129159/il_fullxfull.1833129159_89hg.jpg")
    
    artifact9 = Artifact(culture=south_american, name="Aztec Calendar", era="15th Century", description="Stone calendar of Aztec origin.", image_url="https://i.pinimg.com/originals/21/4c/9f/214c9fd77100770b09b68d9ce0599155.jpg")
    artifact10 = Artifact(culture=south_american, name="Incan Gold Mask", era="16th Century", description="A ceremonial mask made of pure gold.", image_url="https://th.bing.com/th/id/OIP.OGS_7wV4nxt4HRk22y53gwHaE8?w=272&h=181&c=7&r=0&o=5&dpr=1.3&pid=1.7")
    
    artifact11 = Artifact(culture=oceania, name="Tiki Statue", era="19th Century", description="Symbol of spiritual significance.", image_url="https://i.pinimg.com/originals/be/75/96/be75965339294220692da229d169a145.jpg")
    artifact12 = Artifact(culture=oceania, name="Aboriginal Painting", era="18th Century", description="A traditional art form representing stories.", image_url="https://i.pinimg.com/originals/9b/73/86/9b7386af4f4ef53580aa839fbd1ad1b5.jpg")
    
    artifact13 = Artifact(culture=antarctica, name="Scientific Tools", era="Modern Era", description="Used in Antarctic research.", image_url="https://th.bing.com/th/id/OIP.wS2umwmA0erLUwAeAvH4fwHaE8?rs=1&pid=ImgDetMain")
    artifact14 = Artifact(culture=antarctica, name="Ice Core Sample", era="Modern Era", description="A sample revealing Earth's climate history.", image_url="https://www.researchgate.net/profile/Elina-Kari/publication/328214711/figure/fig3/AS:11431281113434529@1673896552258/An-example-of-an-ice-sample-a-ice-core-sample-b-thick-section-1-cm-and-c.png")
    
    db.session.add_all([asian, european, african, north_american, south_american, oceania, antarctica, artifact1, artifact2, artifact3, artifact4, artifact5, artifact6, artifact7, artifact8, artifact9, artifact10, artifact11, artifact12, artifact13, artifact14])
    db.session.commit()

@app.route('/')
def home():
    cultures = Culture.query.all()
    regions_list = [r[0] for r in db.session.query(Culture.region).distinct().all() if r[0]]
    return render_template('home.html', cultures=cultures, regions=regions_list)

@app.route('/culture/<int:culture_id>')
def culture_detail(culture_id):
    culture = Culture.query.get_or_404(culture_id)
    return render_template('culture_detail.html', culture=culture)

@app.route('/search', methods=['GET'])
def search():
    query = request.args.get('q', '')
    region = request.args.get('region', '')
    results = []
    if query:
        results_query = Artifact.query.join(Culture)
        if region:
            results_query = results_query.filter(Culture.region == region)
        results_query = results_query.filter(Artifact.name.ilike(f'%{query}%'))
        results = results_query.all()
    return render_template('search_results.html', query=query, results=results)

@app.route('/api/suggestions', methods=['GET'])
def suggestions():
    query = request.args.get('query', '')
    suggestion_list = []
    if query:
        artifacts = Artifact.query.filter(Artifact.name.ilike(f'%{query}%')).all()
        for art in artifacts:
            suggestion_list.append({'id': art.id, 'name': art.name})
    return jsonify(suggestion_list)

@app.route('/regions')
def regions():
    all_regions = ["Africa", "Antarctica", "Asia", "Europe", "North America", "South America", "Oceania"]
    cultures = Culture.query.all()
    regions_dict = {}
    for culture in cultures:
        region = culture.region or "Unknown"
        if region not in regions_dict:
            regions_dict[region] = []
        regions_dict[region].append(culture)
    for region in all_regions:
        if region not in regions_dict:
            regions_dict[region] = []
    ordered_regions = OrderedDict()
    for region in all_regions:
        ordered_regions[region] = regions_dict[region]
    extra_regions = {r: cults for r, cults in regions_dict.items() if r not in all_regions}
    for key, val in extra_regions.items():
        ordered_regions[key] = val
    return render_template('regions.html', regions_dict=ordered_regions)

if __name__ == '__main__':
    setup_database()
    app.run(debug=True)

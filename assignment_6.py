from flask import Flask, render_template, request, json, jsonify

app = Flask(__name__)

# @ signifies a decorator - way to modifiy
@app.route('/', methods =['GET', 'POST']) #route homepage
def index():
    if request.method == 'POST':
        with open('database.json') as json_file:
            data = json.load(json_file)
            recipes = data["recipes"]
            error_msg = False
            for a_recipe in recipes:
                if a_recipe['recipe_name'] == request.form['search_edit']:
                    return render_template("edit.html", a_recipe = a_recipe)
            if a_recipe['recipe_name'] != request.form['search_edit']:
                error_msg = True
                return render_template("edit.html", error_msg= error_msg)
    else:
        return render_template("index.html")


# using post method to post information from the form.
# using get method to display all recipes.
@app.route('/browse', methods=['POST', 'GET'])
def browse():
    if request.method == 'GET':
        with open('database.json') as json_file:
            recipes = json.load(json_file)
            all_recipes = recipes['recipes']
            nbr_of_recipes = len(all_recipes)
            for recipe_searched in all_recipes:
                return render_template("browse.html", all_recipes = all_recipes, nbr_of_recipes = nbr_of_recipes)

    if request.method == 'POST':
        recipe_name = request.form['recipe_name'].lower()
        ingridient_1 = request.form['firstIngridient']     # store all input from the user.
        ingridient_2 = request.form['secondIngridient']
        ingridient_3 = request.form['thirdIngridient']
        img = request.form['img']
        comment = request.form['comment']
        add_recipe(recipe_name, ingridient_1,ingridient_2,ingridient_3,img,comment) # send all of the info to add_user method.
        return render_template("index.html")



#Appends a new recipe to the json database.
def add_recipe(recipe_name,ingridient_1 , ingridient_2, ingridient_3, img, comment):
    data = {"recipe_name":recipe_name, "ingridient_1":ingridient_1, "ingridient_2":ingridient_2, "ingridient_3":ingridient_3, "img":img, "comment":comment}
    with open('database.json') as json_file:
        recipe = json.load(json_file)
        recipe["recipes"].append(data)
    with open("database.json", "w") as json_file:
        json.dump(recipe, json_file, indent=4) # Indent for visual aid.
    pass


#Used for searching recipes.
@app.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == 'GET':
        with open('database.json') as json_file:
            data = json.load(json_file)
            recipes = data["recipes"]
            for a_recipe in recipes:
                if a_recipe["recipe_name"] == request.args.get('search'):
                    return render_template("recipe.html", a_recipe = a_recipe)


#Route for edit page.
@app.route('/edit')
def edit():
    return render_template("edit.html")

#Route for editing recipies.
@app.route('/update_json/<string:recipe_id>', methods = ['POST'])
def update_json(recipe_id):
    if request.method == 'POST':
        with open('database.json', 'r+') as f:      # Open file r+ for read and append.
            data = json.load(f)
            recipes = data["recipes"]
            for recipe in recipes:
                if recipe_id == recipe['recipe_name']:
                    recipe['recipe_name'] = request.form['recipe_name'].lower()
                    recipe['ingridient_1'] = request.form['firstIngridient']
                    recipe['ingridient_2'] = request.form['secondIngridient']
                    recipe['ingridient_3'] = request.form['thirdIngridient']
                    recipe['img'] = request.form['img']
                    recipe['comment'] = request.form['comment']
                    f.seek(0)                                       #seek to beginning of document.
                    f.write(json.dumps(data, indent=4))             # write the data to jsonfile with indention for visual aid.
                    f.truncate()
                    return render_template("edit.html")


#Api route to see a json recipe in webbrowser.
@app.route('/api/browse/<recipe>') #route a user
def user(recipe):
    with open('database.json') as json_file:
        data = json.load(json_file)
        recipes = data["recipes"]
        for a_recipe in recipes:
            if a_recipe["recipe_name"] == recipe:
                return jsonify(a_recipe)

#Api route to see all json recipes in webbrowser.
@app.route('/api/recipes_all')
def recipes_all():
    with open('database.json') as json_file:
        recipes = json.load(json_file)
        return jsonify(recipes)


# route all pages that doesnt exist here for error handling. 
@app.errorhandler(404) #route 404 page
def page_not_found(e):
    return render_template('404.html'), 404

# only run if your in the main file
if __name__ == "__main__":
    app.run(debug = True)

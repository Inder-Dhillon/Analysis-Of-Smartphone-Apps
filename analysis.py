from csv import reader

#Functions
def explore_data(dataset, start, end, rows_and_columns=False):
    dataset_slice = dataset[start:end]
    for row in dataset_slice:
        print(row)
        print('\n') # adds a new (empty) line after each row

    if rows_and_columns:
        print('Number of rows:', len(dataset))
        print('Number of columns:', len(dataset[0]))

def open_set(file):
    opened_file = open(file, encoding="utf8")
    read_file = reader(opened_file)
    file_list = list(read_file)
    return file_list[0], file_list[1:]

def duplicate_data(dataset):
    duplicate = []
    unique = []
    for data in dataset:
        name = data[0]
        if name in unique:
            duplicate.append(name)
        else:
            unique.append(name)
    return duplicate,unique

def isEnglish(string):
    flag = 0
    for char in string:
        if ord(char) > 127:
            flag +=1
    if flag > 3:
        return False
    return True

def freq_table(dataset, index):
    dictionary = {}
    for data in dataset:
        val = data[index]
        if val in dictionary:
            dictionary[val] += 1
        else:
            dictionary[val] = 1
    return dictionary

def display_table(dataset, index):
    table = freq_table(dataset, index)
    table_display = []
    for key in table:
        key_val_as_tuple = (table[key], key)
        table_display.append(key_val_as_tuple)

    table_sorted = sorted(table_display, reverse = True)
    for entry in table_sorted:
        print(entry[1], ':', round((entry[0]/len(dataset)*100),ndigits=2),'%')

#Opening the two sets
gp_header, gp_store = open_set('googleplaystore.csv')
apple_header, apple_store = open_set('AppleStore.csv')
#Dataset had a bad row - Removing it
del gp_store[10472]
#Checking for duplicates
gp_duplicate, gp_unique = duplicate_data(gp_store)
apple_duplicate, apple_unique = duplicate_data(apple_store)


#Removing duplicates to keep most recent data - Keeping the rows with the most number of reviews
reviews_max= {}
android_clean=[]
already_added=[]
#Forming dictionary with maximum reviews for unique apps
for app in gp_store:
    name = app[0]
    n_reviews = float(app[3])
    if name in reviews_max and reviews_max[name] < n_reviews:
        reviews_max[name] = n_reviews
    elif name not in reviews_max:
        reviews_max[name] = n_reviews
#Cleaning the data-set
for app in gp_store:
    name = app[0]
    n_reviews = float(app[3])
    if n_reviews == reviews_max[name] and name not in already_added:
        android_clean.append(app)
        already_added.append(name)
#Removing non-english apps
for app in android_clean:
    name = app[0]
    if isEnglish(name) == False:
        android_clean.remove(app)
for app in apple_store:
    name = app[1]
    if isEnglish(name) == False:
        apple_store.remove(app)
#Removing paid apps
for app in apple_store:
    price = app[5]
    if price!='0':
        apple_store.remove(app)
for app in android_clean:
    price = app[7]
    if price!='0':
        android_clean.remove(app)
#Genre Data
print("=====> Number of apps per genre\n")
print('=> Android')
display_table(android_clean, 1)
print("\n")
print('=> Apple')
display_table(apple_store,-5)



#User Install Data
print("\nNumber of avg users per genre\n")
print('=> Android')
apple_user_table = freq_table(apple_store, -5)
gp_genre_table = freq_table(android_clean,1)
for genre in apple_user_table:
    total = 0
    len_genre = 0
    for app in apple_store:
        genre_app = app[-5]
        if genre == genre_app:
            user_ratings = float(app[6])
            total += user_ratings
            len_genre += 1
    avg_users = total/len_genre
    print(genre+" : ", avg_users)
print('\n')
print('=> Apple')
for genre in gp_genre_table:
    total = 0
    len_genre = 0
    for app in android_clean:
        genre_app = app[1]
        if genre == genre_app:
            installs = app[5]
            installs = installs.replace('+','')
            installs = installs.replace(',','')
            installs = float(installs)
            total += installs
            len_genre +=1
    avg_users = total / len_genre
    print(genre + " : ", avg_users)




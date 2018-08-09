# #######################################################################################################################################
# Skrypt do czyszczenia contentu i sortowania assetów
#
# Sprawdzony w 4.20.1, nie wiem czy działa w 4.19, ale _POWINIEN_
#
# Jak coś się zjebało to do opierdolenia jest Skubert
#
# Wersja 0.2 prealpha, eksperymentalna jak cały ficzer silnikowy, używasz na własną odpowiedzialność, yadda yadda
# Nie gwarantuje że wszystko sie przerzuci, mnie sie jedna tekstura została, ale na 1.7GB testowego contentu nie jest źle
#
# TODO:
#	* rozróżnianie rodzajów tekstur (normalki do osobnego folderu)
#	* sprawdzanie czy nazwa folderu docelowego jest poprawna
#
# #######################################################################################################################################
#
# Tutaj konfiguruj działanie skryptu
#
# #######################################################################################################################################

# oba foldery ___MUSZĄ___ zaczynać sie od /Game/, jest to root contentbrowsera

# Wszystkie obostrzenia nazw folderów jakie są w contentbrowserze też się tu aplikują, więc NIE SPIERDOL TEGO, sam nie wiem co sie stanie

#zmienna definiująca folder który chcemy ogarnąć
folder = '/Game/'

# Folder w którym będą assety po sortowaniu, BEZ / na końcu
targetFolder = '/Game/Assets'

# Dict z customowymi nazwami folderów dla podanych klas, kluczem jest silnikowa nazwa klasy, wartościa jest 
# nazwa folderu jaką chcemy dla danej klasy. Jeśli klasa nie jest wpisana w tego dicta zostanie stworzony folder 
# z pełną silnikową nazwą klasy, np. StaticMesh lub MaterialParameterCollection
foldernames = {
				"Material" : "Material",
				"MaterialInstanceConstant" : "MaterialInstance",
				"Texture2D" : "Texture",
				"ParticleSystem" : "Particle",
				"SoundCue" : "Sound/Cue",
				"SoundWave" : "Sound/Wave",
				"MaterialParameterCollection" : "MaterialParameters"
			}

# #######################################################################################################################################
# Koniec konfiguracji
#
# Pamiętaj zrobić fix up redirectors na całym contencie i najlepiej zrestartować silnik
#
# Puste foldery niestety musicie usunąć sami, ale dopiero po fixowaniu redirectorów
# #######################################################################################################################################

import unreal

def Clean():
	#Lista wszystkich assetów w folderze
	list = unreal.EditorAssetLibrary.list_assets(folder, include_folder=False)

	# Sprawdzanie jakie klasy są w zadanym folderze
	classes = []
	for i in list:
		if unreal.EditorAssetLibrary.does_asset_exist(list[list.index(i)]):
			classes.append(str(unreal.EditorAssetLibrary.find_asset_data(list[list.index(i)]).asset_class))

	# Tworzymy folder docelowy jesli jakiekolwiek assety istnieją w folderze który czyścimy
	if len(classes)	 > 0:
		unreal.EditorAssetLibrary.make_directory(targetFolder+'/')

	# Konwertujemy listę na set żeby pozbyć się duplikatów, usuwamy niepotrzebne redirectory żeby nie robić zbędnych folderów
	set(classes).remove("ObjectRedirector")
	#tworzymy dicta trzymającego informacje o ilości assetów danej klasy
	encounters = dict.fromkeys(set(classes), 0)

	# Zliczamy ile assetów danej klasy jest w zadanym folderze
	for i in list:
		if unreal.EditorAssetLibrary.find_asset_data(list[list.index(i)]).is_valid() and str(unreal.EditorAssetLibrary.find_asset_data(list[list.index(i)]).asset_class) != "ObjectRedirector":
			encounters[str(unreal.EditorAssetLibrary.find_asset_data(list[list.index(i)]).asset_class)] += 1	

	# Pusty dict na nazwy folderów
	folders = {}
	
	# Tworzymy foldery na poszczególne klasy, jeśli klasa jest zapisana w foldernames to tworzymy folder o nazwie przez nas wybranej, 
	# jeśli nie, tworzymy folder o nazwie samej klasy
	for k, v in encounters.iteritems():
		if v > 0:
			if k in foldernames:
				folders[k] = targetFolder+'/'+foldernames[k]+'/'
				unreal.EditorAssetLibrary.make_directory(targetFolder+'/'+foldernames[k]+'/')
			else:
				folders[k] = targetFolder+'/'+k+'/'
				unreal.EditorAssetLibrary.make_directory(targetFolder+'/'+k+'/')

	# Przenosimy klasy do odpowiednich folderów
	for i in list:
		if unreal.EditorAssetLibrary.does_asset_exist(list[list.index(i)]):
			if unreal.EditorAssetLibrary.find_asset_data(list[list.index(i)]).is_valid():
				assetclass = unreal.EditorAssetLibrary.find_asset_data(list[list.index(i)]).asset_class
				if str(assetclass) != "ObjectRedirector":
					unreal.EditorAssetLibrary.rename_asset(unreal.EditorAssetLibrary.find_asset_data(list[list.index(i)]).object_path, folders[str(assetclass)]+str(unreal.EditorAssetLibrary.find_asset_data(list[list.index(i)]).asset_name))

if folder[0:4] == "/Game" and targetFolder[0:4] == "/Game":
	if targetfolder[:-1] != "/":
		Clean()
	else:
		print "ERROR! Na końcu zmiennej targetFolder ma NIE BYĆ forwardslasha!"
else:
	print "ERROR! Nazwa folderów ma się zaczynać od /Game!"
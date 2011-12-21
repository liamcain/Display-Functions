#Display Functions (Sublime Text 2 Plugin)

###*\*Java Only\**

Description
=========
####Displays an object's methods in autocomplete box.


Usage
=====

Pressing 'period' after an object opens ST2's autocomplete, loaded with all of the objects methods

*\*NOTE\*
if a method is not showing up, make sure that object's file is saved*

###Features
* NEW - Supports 'super'
* NEW - Adds methods of the parent classes
* Supports 'chained' methods:	
    * i.e. `someObj.getVal()|`
* Supports some of Java's default objects (String and Object)
* Offers a very simple way to add more of Java's default objects (for example: if you use Scanner or Random)
    * Just create a txt file with the filename as the Object type, then add `methods = self.check_str(classname, "NAME")` where NAME is the name of file

from django.db import models


class Plant(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100)
    latin_name = models.CharField(max_length=100)
    family = models.CharField(max_length=100)
    food_text = models.TextField(blank=True)
    description = models.TextField()
    medicinal_uses = models.TextField(blank=True)
    warnings = models.TextField()
    poisonous_look_alike = models.TextField(blank=True)
    # Plant Group
    trees = models.BooleanField(default=False)
    shrubs = models.BooleanField(default=False)
    lichens = models.BooleanField(default=False)
    herbs = models.BooleanField(default=False)
    poisonous = models.BooleanField(default=False)
    # Region
    in_colorado = models.BooleanField(default=True)
    in_idaho = models.BooleanField(default=True)
    in_montana = models.BooleanField(default=True)
    in_new_mexico = models.BooleanField(default=True)
    in_utah = models.BooleanField(default=True)
    in_washington = models.BooleanField(default=True)
    in_wyoming = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class Image(models.Model):
    plant = models.ForeignKey(Plant, on_delete=models.CASCADE)
    image_author = models.CharField(max_length=100)
    image_link = models.URLField(max_length=400)
    license = models.CharField(max_length=100)
    image = models.ImageField(upload_to='library/static/images/')

    def __str__(self):
        return self.image.name.split("/").pop()

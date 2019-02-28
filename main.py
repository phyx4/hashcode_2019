import os
from functools import reduce


class Photo:
    id = None
    layout = None  # v or h
    tags = []

    def __init__(self, id, layout, tags):
        self.id = id
        self.layout = layout
        # self.tagalf = "".join(sorted(tags))
        self.tagalf = tuple(sorted(tags))
        self.tags = tags

    def __str__(self):
        return str(self.id) + " - " + " ".join(self.tags)


class Slide:
    # 2 vertical or 1 horizontal
    photo_ids = []
    tags = []

    def __init__(self, photos):
        self.photo_ids = [str(photo.id) for photo in photos]
        self.tags = set(reduce(list.__add__, map(lambda x: list(x.tags), photos)))
        self.tags_sorted = tuple(sorted(list(self.tags)))

    def __str__(self):
        return " ".join([str(x) for x in self.photo_ids]) + " - " + " ".join([str(x) for x in self.tags])


class SlideShow:
    slides = []

    def __init__(self, slides=None):
        self.slides = [] if slides is None else slides

    def calculate_score(self):
        if len(self.slides) == 0:
            return 0
        score = 0
        for i, slide in enumerate(self.slides):
            score += self.interest_factor(i)
        return score

    def interest_factor(self, i):
        if i + 1 >= len(self.slides):
            return 0
        return interest_factor(self.slides[i], self.slides[i + 1])


def interest_factor(slide_1, slide_2):
    """ interest of slides
    Minimum between
    the number of common tags between Si and Si+1
    the number of tags in Si but not in Si+1
    the number of tags in Si+1 but not in Si
    """
    common = set(slide_1.tags) & set(slide_2.tags)
    n_common = len(common)
    n_left = len(slide_1.tags) - len(set(slide_1.tags) & set(common))
    n_right = len(slide_2.tags) - len(set(common) & set(slide_2.tags))
    return min(n_common, n_left, n_right)


def n_common_tags(slide_1, slide_2):
    # return len(set(slide_1.tags) & set(slide_2.tags))
    return len(set(slide_1.tags).intersection(slide_2.tags))


def read_input(filepath):
    with open(filepath, 'r') as f:
        n = int(f.readline())
        i = 0
        result = []
        while i < n:
            line = f.readline()[:-1].split(" ")
            result.append(Photo(i, line[0], line[2:]))
            i += 1
    return result


def write_output(slideshow, output_file):
    with open(output_file, "w") as f:
        f.write(str(len(slideshow.slides)) + "\n")
        for slide in slideshow.slides:
            f.write(' '.join(slide.photo_ids) + "\n")

    with open(output_file, 'rb+') as f:
        f.seek(-2, os.SEEK_END)
        f.truncate()


def get_slideshow(photos):
    slides = []
    vert = None
    for photo in photos:
        if photo.layout == "H":
            slides.append(Slide([photo]))
        elif photo.layout == "V" and vert is None:
            vert = photo
        elif photo.layout == "V" and vert is not None:
            slides.append(Slide([photo, vert]))
            vert = None
    # all_vert_comb = list(itertools.combinations(verticals, 2))
    max_score = 0
    max_perm = None
    # print("Calculating perms of {} elements".format(len(slides)))
    # slides_perms = [list(x) for x in set(itertools.permutations(slides))]
    # print("Trying {} permutations".format(len(slides_perms)))
    # for slides_perm in slides_perms:
    #     score = SlideShow(slides_perm).calculate_score()
    #     max_perm = slides_perm if score > max_score else max_perm
    #     max_score = score if score > max_score else max_score

    print("Calculating perms of {} elements".format(len(slides)))
    slides_perms = itertools.permutations(slides)
    # print("Trying {} permutations".format(len(slides_perms)))
    for slides_perm in slides_perms:
        score = SlideShow(slides_perm).calculate_score()
        max_perm = slides_perm if score > max_score else max_perm
        max_score = score if score > max_score else max_score
    return SlideShow(max_perm)


def main():
    files = ['a_example.txt', 'b_lovely_landscapes.txt', 'c_memorable_moments.txt', 'd_pet_pictures.txt',
             'e_shiny_selfies.txt']
    sum_score = 0
    for file in files:
        print(file)
        photos = read_input(file)
        slideshow = get_slideshow(photos)
        score = slideshow.calculate_score()
        sum_score += score
        print("SCORE: {}\n".format(score))
        write_output(slideshow, "output/" + file)
    print("END, {}".format(sum_score))
    return None


if __name__ == "__main__":
    main()

from .fixtures import TestPosts


class StrModelTest(TestPosts):
    def test_str_post_and_group(self):
        post = self.post
        group = self.group
        comment = self.comment
        self.assertEqual(post.text[:15], str(post))
        self.assertEqual(group.title, str(group))
        self.assertEqual(comment.text, str(comment))

    def test_help_text(self):
        post = self.post
        help_texts = {
            'title': 'Enter the title',
            'text': "Enter text of the posts",
            'group': 'Choice group',
        }
        for field, expected in help_texts.items():
            with self.subTest(field=field):
                self.assertEqual(
                    post._meta.get_field(field).help_text,
                    expected
                )

    def test_verbose_name(self):
        post = self.post
        verbose_names = {
            'text': 'Text of the posts',
            'pub_date': 'Publication date',
            'author': 'Author',
            'group': 'Group',
        }
        for field, expected in verbose_names.items():
            with self.subTest(field=field):
                self.assertEqual(
                    post._meta.get_field(field).verbose_name,
                    expected
                )

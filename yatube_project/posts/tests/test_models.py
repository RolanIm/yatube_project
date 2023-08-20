from .fixtures import TestPosts


class StrModelTest(TestPosts):
    def test_str_post_and_group(self):
        post = self.post
        group = self.group
        self.assertEqual(post.text, str(post))
        self.assertEqual(group.title, str(group))

    def test_help_text(self):
        post = self.post
        help_texts = {
            'text': 'Введите текст поста',
            'group': 'Выберите группу',
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
            'text': 'Текст поста',
            'pub_date': 'Дата публикации',
            'author': 'Автор',
            'group': 'Группа'
        }
        for field, expected in verbose_names.items():
            with self.subTest(field=field):
                self.assertEqual(
                    post._meta.get_field(field).verbose_name,
                    expected
                )

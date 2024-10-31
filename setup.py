from setuptools import setup, find_packages

setup(
    name='codeboot',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        "pygame",
        # Liste des dépendances
    ],
    author='Victorio N.',
    author_email='victorio.nascimento@gmail.com',
    description='Fonctions de Codeboot. Voir doc codeboot',
    long_description_content_type='text/markdown',
    url='https://github.com/Victorio-NASCIMENTO/Fonctions_Codeboot/tree/main',  # Lien vers le dépôt
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)

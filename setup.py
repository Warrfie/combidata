from setuptools import setup, find_packages
import pathlib

here = pathlib.Path(__file__).parent.resolve()
long_description = (here / "README.md").read_text(encoding="utf-8")


setup(
    name="combidata",
    version="0.2.4",
    description="Package for random data generation and combination different cases",
    long_description=open('README.md').read(),
    url="https://warrfie.github.io/combidata",
    author="Kuklikov Maxim (Warrfie)",
    author_email="warrfie@gmail.com",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Information Technology",
        "Topic :: Software Development :: Quality Assurance",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
    ],
    keywords="QA, random data, data generation, testing API, testing, autotesting",
    packages=find_packages(),
    python_requires=">=3.10, <4",
    project_urls={
        "Telegram": "https://t.me/sasisochka",
        "Main page": "https://github.com/Warrfie/combidata"
    },

    long_description_content_type='text/markdown'
)


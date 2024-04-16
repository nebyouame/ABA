from setuptools import setup, find_packages

setup(
    name='ABA',
    version='0.1',
    description='Integrating ERPNext with a Biometric Attendance Machine',
    author='TTSP',
    author_email='nebyouame737@email.com',
    packages=find_packages(),
    install_requires=[
        'frappe',
        'flit_core >=3.4,<4',
        'python = >=3.10'
        # Add any other dependencies here
    ],
    include_package_data=True,
    zip_safe=False,
)
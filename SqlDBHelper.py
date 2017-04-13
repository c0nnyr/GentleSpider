# coding:utf-8
from sqlalchemy import Column, Integer, String, Text, Float, create_engine, and_, or_
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///data.sqlite')
session_marker = sessionmaker(bind=engine)
session = session_marker()

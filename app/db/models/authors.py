from typing import Optional
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import ForeignKey
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = 'users'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    login: Mapped[str] = mapped_column(String(30), nullable=False, unique=True)
    email: Mapped[str] = mapped_column(String(64), nullable=False, unique=True)
    blogs: Mapped[list['Blog']] = relationship('Blog', back_populates='owner')
    posts: Mapped[list['Post']] = relationship('Post', back_populates='author')


class Blog(Base):
    __tablename__ = 'blog'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    owner_id: Mapped[int] = mapped_column(Integer, ForeignKey('users.id'))
    name: Mapped[str] = mapped_column(String(64), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    owner: Mapped['User'] = relationship('User', back_populates='blogs')
    posts: Mapped[list['Post']] = relationship('Post', back_populates='blog')


class Post(Base):
    __tablename__ = 'post'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    header: Mapped[str] = mapped_column(String(128), nullable=False)
    text: Mapped[str] = mapped_column(String, nullable=False)
    author_id: Mapped[int] = mapped_column(Integer, ForeignKey('users.id'))
    blog_id: Mapped[int] = mapped_column(Integer, ForeignKey('blog.id'))
    author: Mapped['User'] = relationship('User', back_populates='posts')
    blog: Mapped['Blog'] = relationship('Blog', back_populates='posts')

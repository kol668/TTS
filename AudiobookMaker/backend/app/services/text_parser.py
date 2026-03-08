import os
import re
from typing import List, Dict
import ebooklib
from ebooklib import epub
from bs4 import BeautifulSoup
import PyPDF2

class TextParser:
    """文本解析器 - 支持多种格式"""
    
    def parse(self, file_path: str) -> str:
        """根据文件类型解析文本"""
        ext = os.path.splitext(file_path)[1].lower()
        
        if ext == '.txt':
            return self._parse_txt(file_path)
        elif ext == '.epub':
            return self._parse_epub(file_path)
        elif ext == '.pdf':
            return self._parse_pdf(file_path)
        else:
            raise ValueError(f"不支持的文件格式: {ext}")
    
    def _parse_txt(self, file_path: str) -> str:
        """解析TXT文件"""
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    
    def _parse_epub(self, file_path: str) -> str:
        """解析EPUB文件"""
        book = epub.read_epub(file_path)
        text_content = []
        
        for item in book.get_items():
            if item.get_type() == ebooklib.ITEM_DOCUMENT:
                soup = BeautifulSoup(item.get_content(), 'html.parser')
                text_content.append(soup.get_text())
        
        return '\n'.join(text_content)
    
    def _parse_pdf(self, file_path: str) -> str:
        """解析PDF文件"""
        text_content = []
        with open(file_path, 'rb') as f:
            pdf_reader = PyPDF2.PdfReader(f)
            for page in pdf_reader.pages:
                text_content.append(page.extract_text())
        return '\n'.join(text_content)
    
    def split_into_paragraphs(self, text: str) -> List[str]:
        """将文本分割成段落"""
        # 按换行符分割
        paragraphs = re.split(r'\n+', text)
        # 过滤空段落
        return [p.strip() for p in paragraphs if p.strip()]

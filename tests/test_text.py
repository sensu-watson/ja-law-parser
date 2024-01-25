from typing import Optional

from ja_law_parser.model import (
    ArticleTitle,
    Fig,
    Line,
    QuoteStruct,
    Sentence,
    TaggedText,
    Text,
    WithArticleTitle,
    WithSentences,
    Item,
    Paragraph,
    List,
    FigStruct,
    Table,
    TableStruct,
    AppdxTable,
    ArithFormula,
    TOCSection,
    Subitem1,
    Subitem2,
    Subitem3,
    Subitem4,
    Subitem5,
    Subitem6,
    Subitem7,
    Subitem8,
    Subitem9,
    Subitem10,
)


class ArticleTitleContainer(WithArticleTitle, tag="ArticleTitleContainer"):
    """
    A virual pydantic-xml model that has the article_title for testing.
    """

    pass


class SentenceContainer(WithSentences, tag="SentenceContainer"):
    """
    A virual pydantic-xml model that has the sentences for testing.
    """

    pass


class TestTaggedText:
    def test_tagged_text_with_line(self) -> None:
        xml = """\
        <ArticleTitleContainer>
          <ArticleTitle>タイトルの<Line Style="dotted"><Ruby>テ<Rt>て</Rt></Ruby></Line><Ruby>ス<Rt>す</Rt></Ruby><Line><Ruby>ト<Rt>と</Rt></Ruby>デー</Line>タ</ArticleTitle>
        </ArticleTitleContainer>
        """  # noqa: E501
        article_title: Optional[ArticleTitle] = ArticleTitleContainer.from_xml(xml).article_title
        assert article_title is not None
        assert article_title.text == "タイトルのテストデータ"

        tagged_text = article_title.tagged_text
        assert tagged_text is not None
        assert len(tagged_text) == 5

        assert type(tagged_text[0]) == Text
        assert tagged_text[0].text == "タイトルの"

        assert type(tagged_text[1]) == Line
        assert tagged_text[1].text == "テ"
        assert tagged_text[1].style == "dotted"
        assert len(tagged_text[1].contents) == 1

        assert type(tagged_text[3]) == Line
        assert tagged_text[3].text == "トデー"
        assert tagged_text[3].style is None
        assert len(tagged_text[3].contents) == 2

        assert type(tagged_text[4]) == Text
        assert tagged_text[4].text == "タ"


class TestQuoteStruct:
    def test_quote_struct_in_sentence(self) -> None:
        xml = """\
        <SentenceContainer>
          <Sentence>AAA<QuoteStruct><Sentence><QuoteStruct><Fig src="url" /></QuoteStruct></Sentence></QuoteStruct> BBB</Sentence>
        </SentenceContainer>
        """  # noqa: E501
        sc: SentenceContainer = SentenceContainer.from_xml(xml)
        assert sc.sentences is not None
        sentences: list[Sentence] = sc.sentences
        assert len(sentences) == 1

        sentence: Sentence = sentences[0]
        assert sentence.text == "AAA BBB"

        assert len(sentence.contents) == 3

        assert type(sentence.contents[0]) == Text
        assert sentence.contents[0].text == "AAA"

        assert type(sentence.contents[1]) == QuoteStruct
        assert len(sentence.contents[1].contents) == 1

        assert type(sentence.contents[1].contents[0]) == Sentence
        sentence2: Sentence = sentence.contents[1].contents[0]
        assert type(sentence2) == Sentence
        assert len(sentence2.contents) == 1

        assert type(sentence2.contents[0]) == QuoteStruct
        quote_struct: QuoteStruct = sentence2.contents[0]
        assert type(quote_struct) == QuoteStruct
        assert len(quote_struct.contents) == 1
        assert type(quote_struct.contents[0]) == Fig
        assert quote_struct.contents[0].src == "url"

        assert type(sentence.contents[2]) == Text
        assert sentence.contents[2].text == " BBB"

    def test_quote_struct_in_line(self) -> None:
        xml = """\
        <ArticleTitleContainer>
          <ArticleTitle><Line><QuoteStruct><Fig src="url" /></QuoteStruct></Line></ArticleTitle>
        </ArticleTitleContainer>
        """
        article_title: Optional[ArticleTitle] = ArticleTitleContainer.from_xml(xml).article_title
        assert article_title is not None

        tagged_text: TaggedText = article_title.tagged_text
        assert tagged_text is not None
        assert len(tagged_text) == 1
        assert type(tagged_text[0]) == Line
        assert len(tagged_text[0].contents) == 1

        quote_struct: QuoteStruct = tagged_text[0].contents[0]
        assert type(quote_struct) == QuoteStruct
        assert len(quote_struct.contents) == 1
        assert type(quote_struct.contents[0]) == Fig
    
    def test_sentence_in_quote_struct_contents(self) -> None:
        xml = """\
        <SentenceContainer>
          <Sentence>
            AAA
            <QuoteStruct>
              AAA
              <Sentence></Sentence>
              BBB
            </QuoteStruct>
            BBB
          </Sentence>
        </SentenceContainer>
        """  # noqa: E501
        sc: SentenceContainer = SentenceContainer.from_xml(xml)
        quote_struct: QuoteStruct = sc.sentences[0].contents[1]
        assert type(quote_struct) == QuoteStruct
        assert len(quote_struct.contents) == 3
        assert type(quote_struct.contents[0]) == Text
        assert type(quote_struct.contents[1]) == Sentence
        assert type(quote_struct.contents[2]) == Text

    def test_item_in_quote_struct_contents(self) -> None:
        xml = """\
        <SentenceContainer>
          <Sentence>
            AAA
            <QuoteStruct>
              AAA
              <Item Num="1">
                <ItemTitle>Item title</ItemTitle>
                <ItemSentence>
                  <Sentence Num="1">Item sentence</Sentence>
                </ItemSentence>
              </Item>
              BBB
            </QuoteStruct>
            BBB
          </Sentence>
        </SentenceContainer>
        """  # noqa: E501
        sc: SentenceContainer = SentenceContainer.from_xml(xml)
        quote_struct: QuoteStruct = sc.sentences[0].contents[1]
        assert type(quote_struct) == QuoteStruct
        assert len(quote_struct.contents) == 3
        assert type(quote_struct.contents[0]) == Text
        assert type(quote_struct.contents[1]) == Item
        assert type(quote_struct.contents[2]) == Text

    def test_paragraph_in_quote_struct_contents(self) -> None:
        xml = """\
        <SentenceContainer>
          <Sentence>
            AAA
            <QuoteStruct>
              AAA
              <Paragraph Num="1">
                <ParagraphNum />
                <ParagraphSentence>
                  <Sentence>Paragraph Sentence</Sentence>
                </ParagraphSentence>
              </Paragraph>
              BBB
            </QuoteStruct>
            BBB
          </Sentence>
        </SentenceContainer>
        """  # noqa: E501
        sc: SentenceContainer = SentenceContainer.from_xml(xml)
        quote_struct: QuoteStruct = sc.sentences[0].contents[1]
        assert type(quote_struct) == QuoteStruct
        assert len(quote_struct.contents) == 3
        assert type(quote_struct.contents[0]) == Text
        assert type(quote_struct.contents[1]) == Paragraph
        assert type(quote_struct.contents[2]) == Text

    def test_list_in_quote_struct_contents(self) -> None:
        xml = """\
        <SentenceContainer>
          <Sentence>
            AAA
            <QuoteStruct>
              AAA
              <List>
                <ListSentence>
                  <Sentence>List sentence</Sentence>
                </ListSentence>
              </List>
              BBB
            </QuoteStruct>
            BBB
          </Sentence>
        </SentenceContainer>
        """  # noqa: E501
        sc: SentenceContainer = SentenceContainer.from_xml(xml)
        quote_struct: QuoteStruct = sc.sentences[0].contents[1]
        assert type(quote_struct) == QuoteStruct
        assert len(quote_struct.contents) == 3
        assert type(quote_struct.contents[0]) == Text
        assert type(quote_struct.contents[1]) == List
        assert type(quote_struct.contents[2]) == Text

    def test_fig_in_quote_struct_contents(self) -> None:
        xml = """\
        <SentenceContainer>
          <Sentence>
            AAA
            <QuoteStruct>
              AAA
              <Fig src="url" />
              BBB
            </QuoteStruct>
            BBB
          </Sentence>
        </SentenceContainer>
        """  # noqa: E501
        sc: SentenceContainer = SentenceContainer.from_xml(xml)
        quote_struct: QuoteStruct = sc.sentences[0].contents[1]
        assert type(quote_struct) == QuoteStruct
        assert len(quote_struct.contents) == 3
        assert type(quote_struct.contents[0]) == Text
        assert type(quote_struct.contents[1]) == Fig
        assert type(quote_struct.contents[2]) == Text

    def test_fig_struct_in_quote_struct_contents(self) -> None:
        xml = """\
        <SentenceContainer>
          <Sentence>
            AAA
            <QuoteStruct>
              AAA
              <FigStruct>
                <Fig src="url" />
              </FigStruct>
              BBB
            </QuoteStruct>
            BBB
          </Sentence>
        </SentenceContainer>
        """  # noqa: E501
        sc: SentenceContainer = SentenceContainer.from_xml(xml)
        quote_struct: QuoteStruct = sc.sentences[0].contents[1]
        assert type(quote_struct) == QuoteStruct
        assert len(quote_struct.contents) == 3
        assert type(quote_struct.contents[0]) == Text
        assert type(quote_struct.contents[1]) == FigStruct
        assert type(quote_struct.contents[2]) == Text

    def test_table_in_quote_struct_contents(self) -> None:
        xml = """\
        <SentenceContainer>
          <Sentence>
            AAA
            <QuoteStruct>
              AAA
              <Table>
                <TableRow>
                  <TableColumn></TableColumn>
                </TableRow>
              </Table>
              BBB
            </QuoteStruct>
            BBB
          </Sentence>
        </SentenceContainer>
        """  # noqa: E501
        sc: SentenceContainer = SentenceContainer.from_xml(xml)
        quote_struct: QuoteStruct = sc.sentences[0].contents[1]
        assert type(quote_struct) == QuoteStruct
        assert len(quote_struct.contents) == 3
        assert type(quote_struct.contents[0]) == Text
        assert type(quote_struct.contents[1]) == Table
        assert type(quote_struct.contents[2]) == Text

    def test_table_struct_in_quote_struct_contents(self) -> None:
        xml = """\
        <SentenceContainer>
          <Sentence>
            AAA
            <QuoteStruct>
              AAA
              <TableStruct>
                <Table>
                  <TableRow>
                    <TableColumn></TableColumn>
                  </TableRow>
                </Table>
              </TableStruct>
              BBB
            </QuoteStruct>
            BBB
          </Sentence>
        </SentenceContainer>
        """  # noqa: E501
        sc: SentenceContainer = SentenceContainer.from_xml(xml)
        quote_struct: QuoteStruct = sc.sentences[0].contents[1]
        assert type(quote_struct) == QuoteStruct
        assert len(quote_struct.contents) == 3
        assert type(quote_struct.contents[0]) == Text
        assert type(quote_struct.contents[1]) == TableStruct
        assert type(quote_struct.contents[2]) == Text

    def test_appdx_table_in_quote_struct_contents(self) -> None:
        xml = """\
        <SentenceContainer>
          <Sentence>
            AAA
            <QuoteStruct>
              AAA
              <AppdxTable></AppdxTable>
              BBB
            </QuoteStruct>
            BBB
          </Sentence>
        </SentenceContainer>
        """  # noqa: E501
        sc: SentenceContainer = SentenceContainer.from_xml(xml)
        quote_struct: QuoteStruct = sc.sentences[0].contents[1]
        assert type(quote_struct) == QuoteStruct
        assert len(quote_struct.contents) == 3
        assert type(quote_struct.contents[0]) == Text
        assert type(quote_struct.contents[1]) == AppdxTable
        assert type(quote_struct.contents[2]) == Text

    def test_arith_formula_in_quote_struct_contents(self) -> None:
        xml = """\
        <SentenceContainer>
          <Sentence>
            AAA
            <QuoteStruct>
              AAA
              <ArithFormula></ArithFormula>
              BBB
            </QuoteStruct>
            BBB
          </Sentence>
        </SentenceContainer>
        """  # noqa: E501
        sc: SentenceContainer = SentenceContainer.from_xml(xml)
        quote_struct: QuoteStruct = sc.sentences[0].contents[1]
        assert type(quote_struct) == QuoteStruct
        assert len(quote_struct.contents) == 3
        assert type(quote_struct.contents[0]) == Text
        assert type(quote_struct.contents[1]) == ArithFormula
        assert type(quote_struct.contents[2]) == Text

    def test_toc_section_in_quote_struct_contents(self) -> None:
        xml = """\
        <SentenceContainer>
          <Sentence>
            AAA
            <QuoteStruct>
              AAA
              <TOCSection Num="1"></TOCSection>
              BBB
            </QuoteStruct>
            BBB
          </Sentence>
        </SentenceContainer>
        """  # noqa: E501
        sc: SentenceContainer = SentenceContainer.from_xml(xml)
        quote_struct: QuoteStruct = sc.sentences[0].contents[1]
        assert type(quote_struct) == QuoteStruct
        assert len(quote_struct.contents) == 3
        assert type(quote_struct.contents[0]) == Text
        assert type(quote_struct.contents[1]) == TOCSection
        assert type(quote_struct.contents[2]) == Text

    def test_subitem1_in_quote_struct_contents(self) -> None:
        xml = """\
        <SentenceContainer>
          <Sentence>
            AAA
            <QuoteStruct>
              AAA
              <Subitem1 Num="1">
                <Subitem1Title>1</Subitem1Title>
                <Subitem1Sentence>
                  <Sentence>Subitem1 Sentence</Sentence>
                </Subitem1Sentence>
              </Subitem1>
              BBB
            </QuoteStruct>
            BBB
          </Sentence>
        </SentenceContainer>
        """  # noqa: E501
        sc: SentenceContainer = SentenceContainer.from_xml(xml)
        quote_struct: QuoteStruct = sc.sentences[0].contents[1]
        assert type(quote_struct) == QuoteStruct
        assert len(quote_struct.contents) == 3
        assert type(quote_struct.contents[0]) == Text
        assert type(quote_struct.contents[1]) == Subitem1
        assert type(quote_struct.contents[2]) == Text

    def test_subitem2_in_quote_struct_contents(self) -> None:
        xml = """\
        <SentenceContainer>
          <Sentence>
            AAA
            <QuoteStruct>
              AAA
              <Subitem2 Num="1">
                <Subitem2Title>1</Subitem2Title>
                <Subitem2Sentence>
                  <Sentence>Subitem2 Sentence</Sentence>
                </Subitem2Sentence>
              </Subitem2>
              BBB
            </QuoteStruct>
            BBB
          </Sentence>
        </SentenceContainer>
        """  # noqa: E501
        sc: SentenceContainer = SentenceContainer.from_xml(xml)
        quote_struct: QuoteStruct = sc.sentences[0].contents[1]
        assert type(quote_struct) == QuoteStruct
        assert len(quote_struct.contents) == 3
        assert type(quote_struct.contents[0]) == Text
        assert type(quote_struct.contents[1]) == Subitem2
        assert type(quote_struct.contents[2]) == Text

    def test_subitem3_in_quote_struct_contents(self) -> None:
        xml = """\
        <SentenceContainer>
          <Sentence>
            AAA
            <QuoteStruct>
              AAA
              <Subitem3 Num="1">
                <Subitem3Title>1</Subitem3Title>
                <Subitem3Sentence>
                  <Sentence>Subitem3 Sentence</Sentence>
                </Subitem3Sentence>
              </Subitem3>
              BBB
            </QuoteStruct>
            BBB
          </Sentence>
        </SentenceContainer>
        """  # noqa: E501
        sc: SentenceContainer = SentenceContainer.from_xml(xml)
        quote_struct: QuoteStruct = sc.sentences[0].contents[1]
        assert type(quote_struct) == QuoteStruct
        assert len(quote_struct.contents) == 3
        assert type(quote_struct.contents[0]) == Text
        assert type(quote_struct.contents[1]) == Subitem3
        assert type(quote_struct.contents[2]) == Text

    def test_subitem4_in_quote_struct_contents(self) -> None:
        xml = """\
        <SentenceContainer>
          <Sentence>
            AAA
            <QuoteStruct>
              AAA
              <Subitem4 Num="1">
                <Subitem4Title>1</Subitem4Title>
                <Subitem4Sentence>
                  <Sentence>Subitem4 Sentence</Sentence>
                </Subitem4Sentence>
              </Subitem4>
              BBB
            </QuoteStruct>
            BBB
          </Sentence>
        </SentenceContainer>
        """  # noqa: E501
        sc: SentenceContainer = SentenceContainer.from_xml(xml)
        quote_struct: QuoteStruct = sc.sentences[0].contents[1]
        assert type(quote_struct) == QuoteStruct
        assert len(quote_struct.contents) == 3
        assert type(quote_struct.contents[0]) == Text
        assert type(quote_struct.contents[1]) == Subitem4
        assert type(quote_struct.contents[2]) == Text

    def test_subitem5_in_quote_struct_contents(self) -> None:
        xml = """\
        <SentenceContainer>
          <Sentence>
            AAA
            <QuoteStruct>
              AAA
              <Subitem5 Num="1">
                <Subitem5Title>1</Subitem5Title>
                <Subitem5Sentence>
                  <Sentence>Subitem5 Sentence</Sentence>
                </Subitem5Sentence>
              </Subitem5>
              BBB
            </QuoteStruct>
            BBB
          </Sentence>
        </SentenceContainer>
        """  # noqa: E501
        sc: SentenceContainer = SentenceContainer.from_xml(xml)
        quote_struct: QuoteStruct = sc.sentences[0].contents[1]
        assert type(quote_struct) == QuoteStruct
        assert len(quote_struct.contents) == 3
        assert type(quote_struct.contents[0]) == Text
        assert type(quote_struct.contents[1]) == Subitem5
        assert type(quote_struct.contents[2]) == Text

    def test_subitem6_in_quote_struct_contents(self) -> None:
        xml = """\
        <SentenceContainer>
          <Sentence>
            AAA
            <QuoteStruct>
              AAA
              <Subitem6 Num="1">
                <Subitem6Title>1</Subitem6Title>
                <Subitem6Sentence>
                  <Sentence>Subitem6 Sentence</Sentence>
                </Subitem6Sentence>
              </Subitem6>
              BBB
            </QuoteStruct>
            BBB
          </Sentence>
        </SentenceContainer>
        """  # noqa: E501
        sc: SentenceContainer = SentenceContainer.from_xml(xml)
        quote_struct: QuoteStruct = sc.sentences[0].contents[1]
        assert type(quote_struct) == QuoteStruct
        assert len(quote_struct.contents) == 3
        assert type(quote_struct.contents[0]) == Text
        assert type(quote_struct.contents[1]) == Subitem6
        assert type(quote_struct.contents[2]) == Text

    def test_subitem7_in_quote_struct_contents(self) -> None:
        xml = """\
        <SentenceContainer>
          <Sentence>
            AAA
            <QuoteStruct>
              AAA
              <Subitem7 Num="1">
                <Subitem7Title>1</Subitem7Title>
                <Subitem7Sentence>
                  <Sentence>Subitem7 Sentence</Sentence>
                </Subitem7Sentence>
              </Subitem7>
              BBB
            </QuoteStruct>
            BBB
          </Sentence>
        </SentenceContainer>
        """  # noqa: E501
        sc: SentenceContainer = SentenceContainer.from_xml(xml)
        quote_struct: QuoteStruct = sc.sentences[0].contents[1]
        assert type(quote_struct) == QuoteStruct
        assert len(quote_struct.contents) == 3
        assert type(quote_struct.contents[0]) == Text
        assert type(quote_struct.contents[1]) == Subitem7
        assert type(quote_struct.contents[2]) == Text

    def test_subitem8_in_quote_struct_contents(self) -> None:
        xml = """\
        <SentenceContainer>
          <Sentence>
            AAA
            <QuoteStruct>
              AAA
              <Subitem8 Num="1">
                <Subitem8Title>1</Subitem8Title>
                <Subitem8Sentence>
                  <Sentence>Subitem8 Sentence</Sentence>
                </Subitem8Sentence>
              </Subitem8>
              BBB
            </QuoteStruct>
            BBB
          </Sentence>
        </SentenceContainer>
        """  # noqa: E501
        sc: SentenceContainer = SentenceContainer.from_xml(xml)
        quote_struct: QuoteStruct = sc.sentences[0].contents[1]
        assert type(quote_struct) == QuoteStruct
        assert len(quote_struct.contents) == 3
        assert type(quote_struct.contents[0]) == Text
        assert type(quote_struct.contents[1]) == Subitem8
        assert type(quote_struct.contents[2]) == Text

    def test_subitem9_in_quote_struct_contents(self) -> None:
        xml = """\
        <SentenceContainer>
          <Sentence>
            AAA
            <QuoteStruct>
              AAA
              <Subitem9 Num="1">
                <Subitem9Title>1</Subitem9Title>
                <Subitem9Sentence>
                  <Sentence>Subitem9 Sentence</Sentence>
                </Subitem9Sentence>
              </Subitem9>
              BBB
            </QuoteStruct>
            BBB
          </Sentence>
        </SentenceContainer>
        """  # noqa: E501
        sc: SentenceContainer = SentenceContainer.from_xml(xml)
        quote_struct: QuoteStruct = sc.sentences[0].contents[1]
        assert type(quote_struct) == QuoteStruct
        assert len(quote_struct.contents) == 3
        assert type(quote_struct.contents[0]) == Text
        assert type(quote_struct.contents[1]) == Subitem9
        assert type(quote_struct.contents[2]) == Text

    def test_subitem10_in_quote_struct_contents(self) -> None:
        xml = """\
        <SentenceContainer>
          <Sentence>
            AAA
            <QuoteStruct>
              AAA
              <Subitem10 Num="1">
                <Subitem10Title>1</Subitem10Title>
                <Subitem10Sentence>
                  <Sentence>Subitem10 Sentence</Sentence>
                </Subitem10Sentence>
              </Subitem10>
              BBB
            </QuoteStruct>
            BBB
          </Sentence>
        </SentenceContainer>
        """  # noqa: E501
        sc: SentenceContainer = SentenceContainer.from_xml(xml)
        quote_struct: QuoteStruct = sc.sentences[0].contents[1]
        assert type(quote_struct) == QuoteStruct
        assert len(quote_struct.contents) == 3
        assert type(quote_struct.contents[0]) == Text
        assert type(quote_struct.contents[1]) == Subitem10
        assert type(quote_struct.contents[2]) == Text

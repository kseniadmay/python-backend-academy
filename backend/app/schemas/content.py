from enum import Enum
from typing import List, Optional
from pydantic import Field
from backend.app.schemas.common import CompatBaseModel


class StepType(str, Enum):
    THEORY = 'THEORY'
    INITIAL_FLASHCARDS = 'INITIAL_FLASHCARDS'
    CODE_PRACTICE = 'CODE_PRACTICE'
    MILESTONE_CHECKPOINT = 'MILESTONE_CHECKPOINT'


class PracticalContrastSnippet(CompatBaseModel):
    language: str = Field(default='python', description='Язык кода')
    code: str = Field(..., description='Эталонный сниппет кода')
    annotation: Optional[str] = Field(default=None, description='Подпись контраста сложности (например, O(1) vs O(N))')


class MicroCheckOption(CompatBaseModel):
    id: str
    text: str


class MicroCheck(CompatBaseModel):
    prompt: str
    options: List[MicroCheckOption]
    correctOptionId: str
    explanation: str


class TheoryStep(CompatBaseModel):
    id: str
    stepType: StepType = StepType.THEORY
    topicTitle: str
    hookHeadline: Optional[str] = None
    hookProblemStatement: Optional[str] = None
    contentMarkdown: str = Field(..., description='Атомарный текст шага (1-3 простых предложения)')
    practicalSnippet: Optional[PracticalContrastSnippet] = None
    backendTakeaway: Optional[str] = None
    rewardXp: int = Field(default=10, description='Награда XP за шаг')


class InitialFlashcard(CompatBaseModel):
    id: str
    question: str
    coreAnswer: str
    badPractice: Optional[str] = None
    goodPractice: Optional[str] = None
    backendInsight: Optional[str] = None


class SocraticHint(CompatBaseModel):
    level: int = Field(..., ge=0, le=3, description='Уровень скаффолдинга 0..3')
    hint: str


class CodeTask(CompatBaseModel):
    id: int
    tier: int = Field(..., ge=1, le=7, description='Уровень сложности 1..7')
    title: str
    description: str
    ioFlow: Optional[str] = Field(default=None, description='Схема входа и выхода (I/O Flow)')
    anatomy: Optional[str] = Field(default=None, description='Анатомия структуры данных / среза')
    initialCode: str
    solutionCode: str
    testCode: str
    hints: List[SocraticHint] = Field(default_factory=list)
    rewardXp: int = Field(default=15)


class Lesson(CompatBaseModel):
    id: str
    title: str
    chapterId: str
    order: int
    steps: List[TheoryStep] = Field(default_factory=list)
    cards: List[InitialFlashcard] = Field(default_factory=list)
    tasks: List[CodeTask] = Field(default_factory=list)

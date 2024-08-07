from typing import Optional

from datahorse.ee.agents.semantic_agent.pipeline.error_correction_pipeline.fix_semantic_schema_prompt import (
    FixSemanticSchemaPrompt,
)
from datahorse.ee.agents.semantic_agent.pipeline.llm_call import LLMCall
from datahorse.helpers.logger import Logger
from datahorse.helpers.query_exec_tracker import QueryExecTracker
from datahorse.pipelines.chat.error_correction_pipeline.error_correction_pipeline_input import (
    ErrorCorrectionPipelineInput,
)
from datahorse.pipelines.pipeline import Pipeline
from datahorse.pipelines.pipeline_context import PipelineContext


class FixSemanticJsonPipeline:
    """
    Error Correction Pipeline to regenerate prompt and code
    """

    _context: PipelineContext
    _logger: Logger

    def __init__(
        self,
        context: Optional[PipelineContext] = None,
        logger: Optional[Logger] = None,
        query_exec_tracker: QueryExecTracker = None,
        on_prompt_generation=None,
        on_code_generation=None,
    ):
        self.pipeline = Pipeline(
            context=context,
            logger=logger,
            query_exec_tracker=query_exec_tracker,
            steps=[FixSemanticSchemaPrompt(), LLMCall()],
        )

        self._context = context
        self._logger = logger

    def run(self, input: ErrorCorrectionPipelineInput):
        self._logger.log(f"Executing Pipeline: {self.__class__.__name__}")
        return self.pipeline.run(input)

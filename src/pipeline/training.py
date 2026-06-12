from src.modelling.train_model import ModellingPipeline
from src.logger import configure_logger

logging = configure_logger()

class TrainingPipeline:
    def __init__(self):
        self.modelling_pipeline = ModellingPipeline()

    def train(self):
        logging.info("Starting training pipeline...")

        self.modelling_pipeline.run()

        logging.info("Training pipeline completed successfully.") 


    

if __name__ == "__main__":
    pipeline = TrainingPipeline()
    pipeline.train()        

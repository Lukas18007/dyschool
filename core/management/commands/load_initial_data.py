from django.core.management.base import BaseCommand
from core.models import Specialization, LessonTopic

class Command(BaseCommand):
    help = 'Load initial data for specializations and lesson topics'

    def handle(self, *args, **options):
        self.stdout.write('Loading initial data...')
        
        # Create specializations
        specializations_data = [
            {
                'name': 'Piano',
                'description': 'Aulas de piano para todos os níveis',
                'topics': [
                    'Técnica Básica',
                    'Leitura de Partitura',
                    'Harmonia',
                    'Improvisação',
                    'Repertório Clássico',
                    'Repertório Popular',
                    'Teoria Musical',
                    'Composição'
                ]
            },
            {
                'name': 'Violão',
                'description': 'Aulas de violão acústico e elétrico',
                'topics': [
                    'Técnica Básica',
                    'Dedilhado',
                    'Harmonia',
                    'Improvisação',
                    'Repertório Popular',
                    'Repertório Clássico',
                    'Teoria Musical',
                    'Composição'
                ]
            },
            {
                'name': 'Canto',
                'description': 'Aulas de canto e técnica vocal',
                'topics': [
                    'Técnica Vocal',
                    'Respiração',
                    'Afinação',
                    'Interpretação',
                    'Repertório Popular',
                    'Repertório Clássico',
                    'Teoria Musical',
                    'Performance'
                ]
            },
            {
                'name': 'Teoria Musical',
                'description': 'Fundamentos da teoria musical',
                'topics': [
                    'Notação Musical',
                    'Ritmo e Compasso',
                    'Escalas',
                    'Harmonia Básica',
                    'Harmonia Avançada',
                    'Análise Musical',
                    'Composição',
                    'Arranjo'
                ]
            },
            {
                'name': 'Bateria',
                'description': 'Aulas de bateria e percussão',
                'topics': [
                    'Técnica Básica',
                    'Rudimentos',
                    'Ritmos Brasileiros',
                    'Rock e Pop',
                    'Jazz',
                    'Improvisação',
                    'Teoria Musical',
                    'Performance'
                ]
            },
            {
                'name': 'Baixo',
                'description': 'Aulas de contrabaixo e baixo elétrico',
                'topics': [
                    'Técnica Básica',
                    'Harmonia',
                    'Walking Bass',
                    'Slap',
                    'Repertório Popular',
                    'Jazz',
                    'Teoria Musical',
                    'Performance'
                ]
            },
            {
                'name': 'Saxofone',
                'description': 'Aulas de saxofone',
                'topics': [
                    'Técnica Básica',
                    'Respiração',
                    'Improvisação',
                    'Repertório Jazz',
                    'Repertório Popular',
                    'Teoria Musical',
                    'Performance',
                    'Manutenção do Instrumento'
                ]
            },
            {
                'name': 'Flauta',
                'description': 'Aulas de flauta transversal',
                'topics': [
                    'Técnica Básica',
                    'Respiração',
                    'Repertório Clássico',
                    'Repertório Popular',
                    'Teoria Musical',
                    'Performance',
                    'Manutenção do Instrumento'
                ]
            }
        ]
        
        for spec_data in specializations_data:
            specialization, created = Specialization.objects.get_or_create(
                name=spec_data['name'],
                defaults={'description': spec_data['description']}
            )
            
            if created:
                self.stdout.write(f'Created specialization: {specialization.name}')
            else:
                self.stdout.write(f'Specialization already exists: {specialization.name}')
            
            # Create lesson topics for this specialization
            for topic_name in spec_data['topics']:
                topic, created = LessonTopic.objects.get_or_create(
                    name=topic_name,
                    specialization=specialization,
                    defaults={'description': f'{topic_name} para {specialization.name}'}
                )
                
                if created:
                    self.stdout.write(f'  - Created topic: {topic.name}')
        
        self.stdout.write(
            self.style.SUCCESS('Successfully loaded initial data!')
        ) 
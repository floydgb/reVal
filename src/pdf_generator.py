"""
PDF Generator for reVal Property Reports
Creates beautiful PDF documents with property valuation data
"""

import os
from datetime import datetime
from typing import Dict, Any
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.platypus.flowables import HRFlowable
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT

class ReValPDFGenerator:
    """Generates professional PDF reports for property valuations"""
    
    def __init__(self, output_dir: str = "./output"):
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
        
        # Set up styles
        self.styles = getSampleStyleSheet()
        self._setup_custom_styles()
    
    def _setup_custom_styles(self):
        """Set up custom paragraph styles"""
        self.styles.add(ParagraphStyle(
            name='CustomTitle',
            parent=self.styles['Heading1'],
            fontSize=24,
            spaceAfter=30,
            alignment=TA_CENTER,
            textColor=colors.HexColor('#2E86AB')
        ))
        
        self.styles.add(ParagraphStyle(
            name='SectionHeader',
            parent=self.styles['Heading2'],
            fontSize=16,
            spaceAfter=12,
            textColor=colors.HexColor('#A23B72')
        ))
        
        self.styles.add(ParagraphStyle(
            name='FactorHeader',
            parent=self.styles['Heading3'],
            fontSize=14,
            spaceAfter=8,
            textColor=colors.HexColor('#F18F01')
        ))
    
    def generate_report(self, property_data: Dict[str, Any], analysis: Dict[str, Any]) -> str:
        """
        Generate a complete reVal property report
        
        Args:
            property_data: Raw property data from Zillow
            analysis: Analyzed data mapped to 10 quality factors
            
        Returns:
            Path to generated PDF file
        """
        # Generate filename
        address = property_data.get('address', 'Unknown Address')
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"reVal_Report_{address.replace(' ', '_')}_{timestamp}.pdf"
        filepath = os.path.join(self.output_dir, filename)
        
        # Create PDF document
        doc = SimpleDocTemplate(
            filepath,
            pagesize=letter,
            rightMargin=72,
            leftMargin=72,
            topMargin=72,
            bottomMargin=18
        )
        
        # Build content
        story = []
        story.extend(self._build_header(property_data))
        story.extend(self._build_property_summary(property_data))
        story.extend(self._build_quality_factors(analysis))
        story.extend(self._build_footer())
        
        # Generate PDF
        doc.build(story)
        return filepath
    
    def _build_header(self, property_data: Dict[str, Any]) -> list:
        """Build the report header"""
        story = []
        
        # Title
        story.append(Paragraph("reVal Property Analysis Report", self.styles['CustomTitle']))
        story.append(Spacer(1, 20))
        
        # Property address
        address = property_data.get('address', 'Address Not Available')
        story.append(Paragraph(f"<b>Property:</b> {address}", self.styles['Normal']))
        story.append(Spacer(1, 10))
        
        # Report date
        report_date = datetime.now().strftime('%B %d, %Y')
        story.append(Paragraph(f"<b>Report Date:</b> {report_date}", self.styles['Normal']))
        story.append(Spacer(1, 20))
        
        # Horizontal line
        story.append(HRFlowable(width="100%", thickness=1, color=colors.grey))
        story.append(Spacer(1, 20))
        
        return story
    
    def _build_property_summary(self, property_data: Dict[str, Any]) -> list:
        """Build property summary section"""
        story = []
        
        story.append(Paragraph("Property Summary", self.styles['SectionHeader']))
        
        # Create summary table
        summary_data = [
            ['Property Type:', property_data.get('propertyType', 'N/A')],
            ['Bedrooms:', str(property_data.get('bedrooms', 'N/A'))],
            ['Bathrooms:', str(property_data.get('bathrooms', 'N/A'))],
            ['Square Feet:', f"{property_data.get('livingArea', 'N/A'):,}" if property_data.get('livingArea') else 'N/A'],
            ['Lot Size:', property_data.get('lotAreaValue', 'N/A')],
            ['Year Built:', str(property_data.get('yearBuilt', 'N/A'))],
            ['Estimated Value:', f"${property_data.get('zestimate', 'N/A'):,}" if property_data.get('zestimate') else 'N/A']
        ]
        
        summary_table = Table(summary_data, colWidths=[2*inch, 3*inch])
        summary_table.setStyle(TableStyle([
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#f0f0f0'))
        ]))
        
        story.append(summary_table)
        story.append(Spacer(1, 30))
        
        return story
    
    def _build_quality_factors(self, analysis: Dict[str, Any]) -> list:
        """Build the 10 quality factors analysis section"""
        story = []
        
        story.append(Paragraph("10 Quality Factors Analysis", self.styles['SectionHeader']))
        story.append(Spacer(1, 15))
        
        factors = [
            'Location', 'Lot Quality', 'Lot Utilization', 'Lot Orientation', 'Privacy',
            'Views', 'Architectural Style', 'Finishes', 'Layout', 'Scale & Volume'
        ]
        
        for i, factor in enumerate(factors, 1):
            factor_data = analysis.get(factor.lower().replace(' ', '_'), {})
            
            story.append(Paragraph(f"{i}. {factor}", self.styles['FactorHeader']))
            
            # Score
            score = factor_data.get('score', 'Not Rated')
            story.append(Paragraph(f"<b>Score:</b> {score}/10", self.styles['Normal']))
            
            # Analysis
            analysis_text = factor_data.get('analysis', 'Analysis not available for this factor.')
            story.append(Paragraph(f"<b>Analysis:</b> {analysis_text}", self.styles['Normal']))
            
            story.append(Spacer(1, 15))
        
        return story
    
    def _build_footer(self) -> list:
        """Build report footer"""
        story = []
        
        story.append(Spacer(1, 30))
        story.append(HRFlowable(width="100%", thickness=1, color=colors.grey))
        story.append(Spacer(1, 10))
        
        footer_text = """
        <i>This report was generated by reVal - Real Estate Valuation Agent.<br/>
        The analysis is based on available property data and market information.<br/>
        For professional real estate advice, consult with a licensed real estate professional.</i>
        """
        
        story.append(Paragraph(footer_text, self.styles['Normal']))
        
        return story

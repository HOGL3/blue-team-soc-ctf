import csv

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
    View,
)
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle

from .forms import ReportForm
from .models import Report


class ReportListView(LoginRequiredMixin, ListView):
    model = Report
    template_name = "reports.html"
    context_object_name = "reports"
    paginate_by = 10

    def get_queryset(self):
        return Report.objects.select_related("incident", "author").order_by(
            "-created_at"
        )


class ReportDetailView(LoginRequiredMixin, DetailView):
    model = Report
    template_name = "report_detail.html"
    context_object_name = "report"

    def get_queryset(self):
        return Report.objects.select_related("incident", "author")


class ReportCreateView(LoginRequiredMixin, CreateView):
    model = Report
    form_class = ReportForm
    template_name = "report_form.html"

    def get_initial(self):
        initial = super().get_initial()
        initial["author"] = self.request.user
        return initial

    def form_valid(self, form):
        form.instance.author = self.request.user
        messages.success(
            self.request, f"Report '{form.instance.title}' created successfully."
        )
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("report_detail", kwargs={"pk": self.object.pk})


class ReportUpdateView(LoginRequiredMixin, UpdateView):
    model = Report
    form_class = ReportForm
    template_name = "report_form.html"

    def form_valid(self, form):
        messages.success(
            self.request, f"Report '{form.instance.title}' updated successfully."
        )
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("report_detail", kwargs={"pk": self.object.pk})


class ReportDeleteView(LoginRequiredMixin, DeleteView):
    model = Report
    template_name = "report_confirm_delete.html"
    success_url = reverse_lazy("reports")

    def delete(self, request, *args, **kwargs):
        report = self.get_object()
        messages.success(request, f"Report '{report.title}' was successfully deleted.")
        return super().delete(request, *args, **kwargs)


# Phase 6B: Export Views
class ReportCSVExportView(LoginRequiredMixin, View):
    def get(self, request, pk):
        report = get_object_or_404(
            Report.objects.select_related("incident", "author"), pk=pk
        )

        response = HttpResponse(content_type="text/csv")
        response["Content-Disposition"] = (
            f'attachment; filename="report_{report.pk}_{timezone.now().strftime("%Y%m%d")}.csv"'
        )

        writer = csv.writer(response)
        # Write headers
        writer.writerow(
            [
                "Report Title",
                "Report Type",
                "Report Status",
                "Author",
                "Related Incident",
                "Created Date",
                "Last Updated",
                "Description",
            ]
        )

        # Write data
        incident_id = report.incident.incident_id if report.incident else "None"
        created_at = report.created_at.strftime("%Y-%m-%d %H:%M:%S")
        updated_at = report.updated_at.strftime("%Y-%m-%d %H:%M:%S")

        writer.writerow(
            [
                report.title,
                report.report_type,
                report.report_status,
                report.author.username,
                incident_id,
                created_at,
                updated_at,
                report.description,
            ]
        )

        return response


class ReportPDFExportView(LoginRequiredMixin, View):
    def get(self, request, pk):
        report = get_object_or_404(
            Report.objects.select_related("incident", "author"), pk=pk
        )

        response = HttpResponse(content_type="application/pdf")
        response["Content-Disposition"] = (
            f'attachment; filename="report_{report.pk}_{timezone.now().strftime("%Y%m%d")}.pdf"'
        )

        # Create PDF document
        doc = SimpleDocTemplate(
            response,
            pagesize=letter,
            rightMargin=72,
            leftMargin=72,
            topMargin=72,
            bottomMargin=18,
        )

        Story = []
        styles = getSampleStyleSheet()

        # Custom styles
        styles.add(
            ParagraphStyle(
                name="CustomTitle",
                parent=styles["Heading1"],
                fontSize=18,
                spaceAfter=20,
            )
        )
        styles.add(
            ParagraphStyle(
                name="Metadata",
                parent=styles["Normal"],
                fontSize=10,
                textColor=colors.dimgrey,
            )
        )
        styles.add(
            ParagraphStyle(
                name="Content",
                parent=styles["Normal"],
                fontSize=11,
                spaceBefore=10,
                spaceAfter=10,
                leading=16,
            )
        )

        # Header
        Story.append(Paragraph("BYTE ME Blue Team Portal", styles["CustomTitle"]))
        Story.append(Paragraph(f"<b>Report:</b> {report.title}", styles["Heading2"]))
        Story.append(Spacer(1, 10))

        # Metadata Table
        incident_str = report.incident.incident_id if report.incident else "None"
        data = [
            ["Report Type:", report.report_type, "Status:", report.report_status],
            ["Author:", report.author.username, "Linked Incident:", incident_str],
            [
                "Created:",
                report.created_at.strftime("%Y-%m-%d %H:%M"),
                "Updated:",
                report.updated_at.strftime("%Y-%m-%d %H:%M"),
            ],
        ]

        t = Table(data, colWidths=[1.2 * inch, 2 * inch, 1.2 * inch, 2 * inch])
        t.setStyle(
            TableStyle(
                [
                    ("BACKGROUND", (0, 0), (-1, -1), colors.whitesmoke),
                    ("TEXTCOLOR", (0, 0), (-1, -1), colors.black),
                    ("ALIGN", (0, 0), (-1, -1), "LEFT"),
                    ("FONTNAME", (0, 0), (-1, -1), "Helvetica"),
                    ("FONTSIZE", (0, 0), (-1, -1), 10),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
                    ("TOPPADDING", (0, 0), (-1, -1), 8),
                    ("GRID", (0, 0), (-1, -1), 0.5, colors.lightgrey),
                    ("FONTNAME", (0, 0), (0, -1), "Helvetica-Bold"),
                    ("FONTNAME", (2, 0), (2, -1), "Helvetica-Bold"),
                ]
            )
        )
        Story.append(t)
        Story.append(Spacer(1, 20))

        # Description
        Story.append(Paragraph("<b>Description</b>", styles["Heading3"]))
        Story.append(Spacer(1, 5))

        # Handle line breaks in description
        for paragraph in report.description.split("\n"):
            if paragraph.strip():
                Story.append(Paragraph(paragraph, styles["Content"]))

        Story.append(Spacer(1, 30))
        Story.append(
            Paragraph(
                f"<i>Report generated on {timezone.now().strftime('%Y-%m-%d %H:%M:%S UTC')}</i>",
                styles["Metadata"],
            )
        )

        # Build PDF with footer
        def add_footer(canvas, doc):
            canvas.saveState()
            canvas.setFont("Helvetica", 9)
            canvas.drawString(
                inch, 0.75 * inch, "BYTE ME Blue Team Portal - Confidential"
            )
            canvas.drawRightString(7.5 * inch, 0.75 * inch, f"Page {doc.page}")
            canvas.restoreState()

        doc.build(Story, onFirstPage=add_footer, onLaterPages=add_footer)
        return response

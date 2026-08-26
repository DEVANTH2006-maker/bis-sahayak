"""Certification and Hallmarking structured guide flows."""

from __future__ import annotations

from app.models.schemas import CertStep, CertificationGuide


# ── Structured certification knowledge (hardcoded for demo, expandable via RAG) ──

CERTIFICATION_SCHEMES = {
    "isi": {
        "name": "ISI Mark (BIS Certification)",
        "description": "Mandatory for products listed under BIS compulsory certification schemes. The ISI mark indicates conformity to relevant Indian Standards.",
        "steps": [
            CertStep(step_number=1, title="Identify the applicable Indian Standard",
                     description="Determine which IS number applies to your product. Check the BIS compulsory certification list or use this assistant's recommendation feature.",
                     tips="Common product categories: electrical appliances (IS 302), cement (IS 455), steel (IS 2062), toys (IS 9873)."),
            CertStep(step_number=2, title="Check if your product requires mandatory certification",
                     description="Check whether your product falls under the Compulsory Registration Scheme (CRS) or Scheme I/II of BIS. Some products require mandatory certification while others are voluntary.",
                     tips="Visit bis.gov.in > Conformity Assessment > Product Certification for the latest list."),
            CertStep(step_number=3, title="Apply to BIS",
                     description="Submit application to BIS through the Manak Online portal (manakonline.bis.gov.in). Create an account, fill in the application form, and upload required documents.",
                     tips="Keep ready: Company registration, factory address proof, product test reports, manufacturing process details."),
            CertStep(step_number=4, title="Factory inspection",
                     description="BIS will conduct a factory inspection to verify manufacturing capability, quality control infrastructure, and compliance with the standard.",
                     tips="Ensure your QC lab, testing equipment, and documentation are in order before the inspection."),
            CertStep(step_number=5, title="Product testing",
                     description="Submit product samples to a BIS-recognized laboratory for testing. The lab will test against the applicable IS standard parameters.",
                     tips="Use this assistant's Lab Lookup feature to find the nearest BIS-recognized lab."),
            CertStep(step_number=6, title="Grant of license",
             description="Once factory inspection and testing are satisfactory, BIS grants the license to use the ISI mark. You receive a certificate with a license number.",
             tips="The license is valid for one year and must be renewed annually."),
            CertStep(step_number=7, title="Ongoing compliance",
                     description="BIS conducts periodic surveillance inspections and re-testing to ensure continued compliance. Maintain quality records.",
                     tips="Non-compliance can lead to suspension or cancellation of the license."),
        ],
        "estimated_time": "2-4 months (varies by product complexity)",
        "documents_required": [
            "Application form (Manak Online)",
            "Company registration / incorporation certificate",
            "Factory address proof (rent agreement / property tax receipt)",
            "Manufacturing process flow chart",
            "Quality control test reports",
            "Product samples for testing",
            "NABL-accredited lab test reports (if available)",
        ],
    },
    "crs": {
        "name": "Compulsory Registration Scheme (CRS)",
        "description": "For products like electronics and IT equipment that require mandatory registration before sale in India.",
        "steps": [
            CertStep(step_number=1, title="Check product eligibility",
                     description="Verify if your product is in the CRS product list (Schedule-I of Electronics and IT Goods Order). Common products: laptops, TVs, LED lights, mobile phones, power adapters.",
                     tips="The CRS list is updated periodically — check the latest MEITY/BIS notification."),
            CertStep(step_number=2, title="Get product tested",
                     description="Get your product tested from a BIS-recognized NABL-accredited laboratory for the applicable IS standard.",
                     tips="Testing must be done from a lab recognized under the CRS scheme specifically."),
            CertStep(step_number=3, title="Register on Manak Online",
                     description="Create an account on manakonline.bis.gov.in and submit the CRS application with test reports.",
                     tips="Upload clear scans of test reports — incomplete applications are rejected."),
            CertStep(step_number=4, title="Obtain registration number",
                     description="Upon verification, BIS assigns a registration number. This number must appear on the product and packaging.",
                     tips="The registration number format: R-XXXXXXXXXXXX (14 digits)."),
            CertStep(step_number=5, title="Label the product",
                     description="Affix the BIS standard mark with the registration number on the product and its packaging.",
                     tips="Use the prescribed marking format — incorrect marking is a violation."),
        ],
        "estimated_time": "1-3 months",
        "documents_required": [
            "Product test reports from BIS-recognized lab",
            "Application form via Manak Online",
            "Company authorization letter",
            "Product photographs",
            "Manufacturing details",
        ],
    },
    "hallmarking": {
        "name": "BIS Hallmarking Scheme",
        "description": "Hallmarking certifies the purity of gold and silver jewelry. Since June 2021, hallmarking of gold jewelry has been made mandatory in a phased manner across India.",
        "steps": [
            CertStep(step_number=1, title="Register as an Assaying and Hallmarking Centre (AHC)",
                     description="Establish or get affiliated with a BIS-recognized Assaying and Hallmarking Centre. AHCs must be NABL-accredited.",
                     tips="Minimum infrastructure: XRF testing machine, fire assay equipment, trained staff."),
            CertStep(step_number=2, title="BIS License for AHC",
                     description="Apply to BIS for a license to operate as an AHC. BIS verifies equipment, staff competence, and premises.",
                     tips="License under Scheme IX of BIS Conformity Assessment Scheme."),
            CertStep(step_number=3, title="Jeweler registration",
                     description="Jewelers must register with BIS to get their jewelry hallmarked. They submit an application with business details.",
                     tips="Registration is free for jewelers. Visit hallmarking.bis.gov.in."),
            CertStep(step_number=4, title="Hallmarking process",
                     description="The jeweler sends jewelry to a BIS-recognized AHC. The center determines purity using XRF/acid testing, then applies the hallmark.",
                     tips="Hallmark includes: BIS logo, purity grade (e.g., 22K916), AHC mark, jeweler's mark, and HUID."),
            CertStep(step_number=5, title="HUID (Hallmark Unique Identification)",
                     description="Each hallmarked item gets a unique 6-digit alphanumeric HUID. Consumers can verify purity using the 'Verify HUID' feature on BIS Care app or bis.gov.in.",
                     tips="HUID is mandatory since April 2023. It ensures traceability of every hallmarked item."),
            CertStep(step_number=6, title="Consumer verification",
                     description="Consumers can verify hallmark authenticity using the BIS Care app or bis.gov.in/hallmarking. Enter the HUID to see purity details and jeweler info.",
                     tips="Always ask for the HUID and verify it before purchasing gold/silver jewelry."),
        ],
        "estimated_time": "1-2 months for jeweler registration (AHC setup: 3-6 months)",
        "documents_required": [
            "Jeweler registration application",
            "GST registration certificate",
            "PAN card of the firm",
            "Shop license / trade license",
            "ID proof of authorized person",
        ],
    },
}


HALLMARKING_FAQS = [
    {"question": "What is hallmarking?", "answer": "Hallmarking is the accurate determination and official recording of the proportional content of precious metal in jewelry or artifacts. In India, BIS hallmarking certifies the purity of gold and silver."},
    {"question": "What is HUID?", "answer": "HUID (Hallmark Unique Identification) is a unique 6-digit alphanumeric code assigned to every hallmarked jewelry item. It allows consumers to verify the purity and authenticity of their gold/silver through the BIS Care app or bis.gov.in."},
    {"question": "How do I verify my jewelry's hallmark?", "answer": "Use the BIS Care app (available on Android/iOS) or visit bis.gov.in/hallmarking. Enter the HUID code stamped on your jewelry to verify purity grade, jeweler details, and AHC information."},
    {"question": "Is hallmarking mandatory in India?", "answer": "Yes, hallmarking of gold jewelry and artifacts has been made mandatory in a phased manner across India since June 2023. Currently it is mandatory in all districts of India for gold of 14, 18, 20, 22, 23, and 24 carat."},
    {"question": "What purity grades are available?", "answer": "Gold hallmarking is available for 24K (999), 23K (958), 22K (916), 20K (833), 18K (750), and 14K (585). The most common for jewelry is 22K (916). Silver hallmarking is available for 999 (fine silver) and 925 (sterling silver)."},
    {"question": "What if my jewelry fails hallmarking?", "answer": "If the AHC determines the purity is less than what the jeweler claimed, the hallmarking will not be applied. You should complain to the jeweler and can also file a complaint on the BIS portal or consumer forum."},
    {"question": "Where can I get my jewelry hallmarked?", "answer": "Visit any BIS-recognized Assaying and Hallmarking Centre (AHC). You can find nearby AHCs on bis.gov.in or the BIS Care app. Some jewelers also offer hallmarking services through their tie-ups with AHCs."},
]


def get_certification_guide(scheme: str = "isi", product_type: str = "") -> CertificationGuide | None:
    """Get structured certification guide for a given scheme."""
    scheme_data = CERTIFICATION_SCHEMES.get(scheme.lower())
    if not scheme_data:
        return None
    return CertificationGuide(
        scheme=scheme_data["name"],
        product_type=product_type or scheme_data["description"],
        steps=scheme_data["steps"],
        estimated_time=scheme_data["estimated_time"],
        documents_required=scheme_data["documents_required"],
    )


def get_hallmarking_faq(query: str = "") -> list[dict]:
    """Get hallmarking FAQs, optionally filtered by keyword match."""
    if not query:
        return HALLMARKING_FAQS
    query_lower = query.lower()
    return [faq for faq in HALLMARKING_FAQS if any(w in faq["question"].lower() + faq["answer"].lower() for w in query_lower.split())]

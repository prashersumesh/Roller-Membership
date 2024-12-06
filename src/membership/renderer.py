import os
import sys
from fpdf import FPDF
from fpdf.fonts import FontFace

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath(".")

    full_path = os.path.join(base_path, relative_path)
    # print(f"Looking for {relative_path} in {full_path}")  # Debug print
    return full_path


class PDF(FPDF):
    def chapter_title(self, title):
        self.set_font("Arial", "B", 12)
        self.cell(10, 10, title, 0, 1, "L")

    def chapter_body(self, body):
        self.set_font("Arial", "", 12)
        self.multi_cell(0, 6, body)


aero_bg = (44, 135, 228)
text_color = (255, 255, 255)


def get_pdf(data):
    pdf = PDF()

    pdf.add_page()
    # pdf.set_font("Times", size= 16)
    pdf.image(resource_path("src/membership/static/aero_no_bg.png"), x=70, y=10, w=0, h=30)

    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 27, "", 0, 1, "C")

    pdf.cell(0, 27, "2679 Bristol Cir, Oakville, ON L6H 6Z8", 0, 1, "C")
    pdf.cell(0, 27, "Membership Agreement Form", 0, 1, "C")
    personal_info = [
        ["Personal Information", ""],
        ["Name", data["name"]],
        ["Phone", data["phone"]],
        ["Email", data["email"]],
        ["Address", data["address"]],
    ]

    booking_membership_info = [
        ["Booking Information", ""],
        ["Membership", data["membership"]],
        [
            "Booking ID",
            data["booking_id"],
        ],
        ["Booking Date", data["booking_date"]],
        [
            "Paid up to",
            data["paid_up_to"],
        ],
        ["Status", data["status"]],
        ["Fees", data["fees"]],
        ["Inventory", data["inventory"]],
        ["Form Status", data["form_status"]],
        ["Transaction ID", data["transction_id"]],
        ["Payment Type", data["payment_type"]],
        ["Booking Total", data["booking_total"]],
        [
            "Discount",
            data["discount"],
        ],
    ]

    headings_style = FontFace(color=text_color, fill_color=aero_bg)
    with pdf.table(headings_style=headings_style) as table:
        for data_row in personal_info:
            row = table.row()
            for datum in data_row:
                row.cell(datum)

    headings_style = FontFace(color=text_color, fill_color=aero_bg)
    with pdf.table(headings_style=headings_style) as table:
        for data_row in booking_membership_info:
            row = table.row()
            for datum in data_row:
                row.cell(datum)

    pdf.add_page()
    # Add agreement details
    agreement_details = """
    Agreement: A. This Membership Agreement consists of provisions A through G below as well as the Additional Terms and Conditions (this "Agreement") and governs your membership in the Aerosports Membership Program that you have selected (the "Program"). Throughout this Agreement, we will refer to as "you" or "Member" and to us as "we" or "Aerosports." This Agreement is important and affects your legal rights, so please read it carefully. Note that Section 14 of the Additional Terms and Conditions contains a mandatory arbitration provision that requires the use of arbitration on an individual basis and limits the remedies available to you in the event of certain disputes.\n
    B. HOME PARK. Aerosports London and Aerosports Oakville offers a monthly membership. Please see the attached Membership Benefits page for more information about the membership options. MEMBERSHIPS ARE ONLY VALID AT THIS SPECIFIC AEROSPORTS LOCATIONS.\n
    C. COMMITMENT. Each Program membership requires a minimum twelve-month commitment, which will automatically renew on a month-to-month or annually basis (based on payment frequency) at the end of the commitment period, unless canceled in accordance with this Agreement. The membership includes a 12-month price guarantee. All Program memberships are non-transferable, and prices are subject to change after 12 months, with 30-days prior notice.\n
    D. TERM. The initial term of your Aerosports membership in the Program begins on the initial date of purchase. Thereafter your Program membership will automatically renew and continue on a month-to-month or annual basis until you expressly cancel it, or until we terminate it, in accordance with the Automatic Renewal Terms set forth below.\n
    E. AUTO RENEWAL. BEFORE THE END OF THE INITIAL 12-MONTH MEMBERSHIP PERIOD, AND EACH MONTH/YEAR THEREAFTER (UNLESS YOU CANCEL YOUR MEMBERSHIP WITH AT LEAST 2 MONTHS NOTICE) WE WILL AUTOMATICALLY RENEW YOUR MEMBERSHIP FOR ANOTHER MONTHLY OR ANNUAL TERM, BASED ON THE ORIGINAL TERMS OF PURCHASE, BY CHARGING THE MEMBERSHIP PRICE IN EFFECT AT THE TIME OF RENEWAL TO YOUR PAYMENT METHOD ON FILE. IF YOU DO NOT WANT TO AUTO-RENEW FOR ANOTHER TERM, YOU NEED TO PROVIDE 2 MONTHS NOTICE BY ONE OF THE FOLLOWING METHODS: a. WRITING TO US AT THE MAILING ADDRESS ON THE TOP RIGHT CORNER OF THIS AGREEMENT WITH A CLEAR INDICATION OF YOUR DESIRE TO CANCEL YOUR MEMBERSHIP. b. VISIT US IN PARK OR EXPRESSING YOUR DESIRE TO CANCEL VIA DETAILED WRITTEN STATEMENT.\n
    F. FREE TRIALS. From time to time, Aerosports may offer free trials of certain subscriptions for specified periods. If we offer you a free trial, we will provide to you the specific terms of the free trial in the marketing materials describing the particular trial or at registration. Free trials are limited to one (1) per household. ONCE YOUR FREE TRIAL ENDS, WE (OR OUR THIRD-PARTY PAYMENT PROCESSOR) WILL BEGIN BILLING YOUR DESIGNATED PAYMENT METHOD ON A RECURRING BASIS FOR YOUR SUBSCRIPTION (PLUS ANY APPLICABLE TAXES AND OTHER FOR AS LONG AS YOUR SUBSCRIPTION CONTINUES, UNLESS YOU CANCEL YOUR SUBSCRIPTION PRIOR TO THE END OF YOUR FREE TRIAL. INSTRUCTIONS FOR CANCELING YOUR SUBSCRIPTION ARE DESCRIBED ABOVE. PLEASE NOTE THAT YOU WILL NOT RECEIVE A NOTICE FROM US THAT YOUR FREE TRIAL HAS ENDED OR THAT THE PAID PORTION OF YOUR SUBSCRIPTION HAS BEGUN. WE RESERVE THE RIGHT TO MODIFY OR TERMINATE FREE TRIALS AT ANY TIME, WITHOUT NOTICE AND IN OUR SOLE DISCRETION.\n
    G. AGREEMENT: By signing this Agreement, you represent, or acknowledge and agree (as the case may be), that: (i) you have the authority to bind all of the members listed above to this Agreement; (ii) all members listed above will be regarded as active members until you cancel each member, in accordance with the cancelation terms stated below. NOTE: you must identify each member whose membership you want to cancel; Aerosports will NOT automatically cancel all listed members; (iii) you will promptly notify Aerosports of any change in your account information; (iv) you are an authorized user of the account used to purchase this membership, and you will not dispute the scheduled transactions with your bank or credit card company so long as the amounts charged are in accordance with the terms and conditions of this Agreement; (v) you understand that Aerosports will not charge you a fee for authorizing recurring payments, but that your financial institution may charge you a fee for accepting and processing electronic debit transactions; (vi) you understand that you have the right to cancel this Agreement within one (1) business day of the date first written above to receive a refund of any pre-paid fees. The refund amount will be subject to additional charges for discounts or perks used during that 24-hour period. Refunds will be processed within thirty Operating Days of receipt of the cancellation notice by Aerosports. "Operating Day" means any day on which patrons may inspect and use the facilities and services of the Aerosports park that issued your Program membership.\n
    """
    pdf.chapter_title("Terms and conditions")
    pdf.chapter_title("AGREEMENT DETAILS")
    pdf.chapter_body(agreement_details)

    # Add the tick image (adjust x, y, width, and height as needed)
    pdf.image(
        resource_path("src/membership/static/tick_image.png"), x=10, y=183.5, w=7, h=7
    )  # Adjust the position (x, y) as needed

    # # Add the text "I agree to all terms and conditions" below the tick image
    pdf.set_xy(20, 182.5)  # Adjust the x, y coordinates to be aligned with the tick
    pdf.set_font("Arial", "", 12)
    pdf.cell(
        0,
        10,
        "I agree to the Duration, Termination, Eligibility and Conditions of the Membership *",
        0,
        1,
    )

    agreement_details = """
    DURATION OF MEMBERSHIP: All memberships have a minimum commitment of twelve months from the Start Date (or if no Start Date is specified, then the date of this Agreement). After the 12-month period, Aerosports will continue to bill you, until you cancel membership in accordance with the cancellation procedure specified above, or unless Aerosports terminates this Agreement, at its sole option. If you would like to cancel during the initial 12-month term after the initial 24-hour period, you will be charged the remaining balance of your 12-month membership. Payments are nonrefundable and there are no refunds or credits for partially used periods. However, you will continue to have access to the Aerosports park associated with your Membership through the end of the initial 12-month period.\n
    ELIGIBILITY AND CONDITIONS: Each Member may be required to show ID for him/herself that is associated with his/her liability waiver on file with Aerosports, for identification purposes. Liability waivers are valid one (1) year from signing, therefore to remain an active Member you must update your liability waiver every year. Also, to remain active. Aerosports reserves the right to request additional forms of identification verification. All questions or disputes regarding an individual's eligibility, the earning/use/conversion of credits, or a Member's compliance with this Agreement will be resolved by Aerosports in its sole discretion.\n
    TERMINATION: Aerosports reserves the right to cancel, suspend or revoke any membership or deny park admission to any Members at any time for any reason. Cancellation, suspension or revocation of park privileges under the Program due to your violation of Aerosports policies or rules, may, at Aerosports sole discretion, result in you being barred from visiting any and all other Aerosports locations without any refund of prepaid fees.\n
    """
    pdf.chapter_body(agreement_details)

    # Add the tick image (adjust x, y, width, and height as needed)
    pdf.image(
        resource_path("src/membership/static/tick_image.png"), x=10, y=82, w=7, h=7
    )  # Adjust the position (x, y) as needed

    # # Add the text "I agree to all terms and conditions" below the tick image
    pdf.set_xy(20, 81)  # Adjust the x, y coordinates to be aligned with the tick
    pdf.set_font("Arial", "", 12)
    pdf.cell(0, 10, "I agree to all the Terms & Conditions *", 0, 1)

    agreement_details = """
    1. UPGRADES: A Member wishing to upgrade his/her membership, if upgrades are available, must choose a membership of equal or greater value than the original Park membership, and the difference in prices shall be due on the day of the upgrade. Each guest wishing to upgrade his/her ticket to a membership must be present at the time of the upgrade transaction and request the upgrade on the same day of purchase. Downgrades are not allowed during the initial 12-month period. You can downgrade your membership after the initial 12-month period, which shall be effective on the next billing period.\n
    2. ADDRESS CHANGE: You must promptly report to Aerosports in writing a change in your address. Changes can be made only by updating your information at the park or by phone.\n
    3. PRIVACY: Please review Aerosports Privacy Policy, which may be found here: www. aerosportsparks.ca for information about how we collect, use and disclose information about you as part of the Program. By enrolling in the Program, you acknowledge that you have read Aerosports Privacy Policy as well as the Safety Policy.\n
    4. CERTAIN LIMITS AND RESTRICTIONS: Discounts included in your Program membership cannot be combined with any other offers, deals, discounts, or promotions. Discounted jump times may be walk-in only if the particular park in question allows it. You must purchase additional jump time at regular prices. Unless otherwise expressly specified, membership does not provide discounts on certain private events (including team parties, corporate events, group events, or facility rentals) or events that require separate admission such as TODDLER TIMES. Membership does not guarantee admission, especially during high attendance or other closure periods. Memberships are nonrefundable, nontransferable and remain the property of Aerosports. Additionally, memberships may not be used for commercial purposes.\n
    5. CHANGES: Aerosports reserves the right in its sole discretion to modify or update this Agreement and/or change, alter, or discontinue the Program, the list of participating parks, parks services, entertainment or attractions, operating hours, and any reward or special status programs at any time and without notice to members beyond updating this Agreement. If we make changes, we will attempt to provide reasonable notice of such changes, such as by sending an email notification or posting an announcement on our website or the website of the park that issued your Program membership.\n
    6. TAXES: The Program, as well as any prize or gift provided to a Member, may be taxable, depending on the value of the item and the applicable federal, provincial, and local tax laws. Members are solely responsible for payment of any applicable taxes and any applicable tax reporting obligations.\n
    7. ASSUMPTION; INDEMNIFICATION AND RELEASE OF LIABILITY: By participating in the Program, you assume the inherent risks associated with the operation of all rides and attractions and should read and obey all safety signage, instructions and rules. In addition, you hereby release Aerosports, its parent, affiliates, franchisees, divisions, related companies, third-party prize/reward providers and suppliers, and agents, and its and their respective officers, directors, owners, and employees, (each a "Releasee") from any and all losses, harm, damages, cost, or expense, whether known or unknown, including without limitation property damages, personal injury, and/or death, arising from or connected to the Program, including, without limitation, (i) the collection, redemption, revocation, or deletion of credits, (ii) the issuance of reward vouchers and use of Program, (iii) the suspension, termination, or modification of your membership or account, and (iv) the suspension, modification, or termination of the Program or any reward or special status programs therein. In addition, you agree to defend, indemnify, and hold harmless the Releases from all liabilities, claims, damages, costs, and expenses (including reasonable attorneys' fees) that arise out of or are related to your violation of this Agreement. Furthermore, you agree to reimburse Aerosports for any Program benefits, if you fraudulently obtained them.\n
    8. YOU ACCEPT THE SERVICES "AS IS." The Program, membership therein, and all prizes, merchandise, sweepstakes, contests, products or services provided through the Program are provided and must be accepted on an "as is" and "as available" basis without warranties of any kind. AEROSPORTS, AEROSPORTS PARTNERS OR ADMINISTRATORS, AND EACH OF THEIR RESPECTIVE AGENTS OR REPRESENTATIVES MAKE NO REPRESENTATIONS OR WARRANTIES, EXPRESS OR IMPLIED, AND DISCLAIM ANY AND ALL LIABILITY AS TO THE CONDITION, QUALITY, MERCHANTABILITY, OR FITNESS FOR A PARTICULAR PURPOSE OF PRODUCTS AND/OR SERVICES PROVIDED BY OR THROUGH THE PROGRAM INCLUDING, WITHOUT LIMITATION, IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE AND ANY WARRANTY OF NON-INFRINGEMENT, TITLE, OR QUIET ENJOYMENT.\n
    9. LIMITATION OF LIABILITY: UNDER NO CIRCUMSTANCES SHALL ANY OF THE RELEASEES BE LIABLE FOR ANY DIRECT, INDIRECT, PUNITIVE, INCIDENTAL, SPECIAL, OR CONSEQUENTIAL DAMAGES ARISING OUT OF OR IN ANY WAY CONNECTED WITH THE PROGRAM OR YOUR PARTICIPATION THEREIN, INCLUDING, WITHOUT LIMITATION, ANY PROGRAM PRIZES, MERCHANDISE, OR SERVICES MADE AVAILABLE AS PART OF THE PROGRAM. IN ANY EVENT, ANY LIABILITY OF AEROSPORTS ARISING IN CONNECTION WITH THE PROGRAM WILL BE LIMITED TO THE GREATER OF (A) THE MEMBERSHIP FEES PAID TO AEROSPORTS (EXCLUDING TAXES) IN THE PREVIOUS TWELVE (12) MONTHS, AND (B) ONE HUNDRED DOLLARS ($100). THIS LIMITATION APPLIES WHETHER THE ALLEGED LIABILITY IS BASED ON CONTRACT, TORT, NEGLIGENCE, STRICT LIABILITY, OR OTHER LEGAL THEORY, EVEN IF THE RELEASEE HAS BEEN ADVISED OF THE POSSIBILITY OF SUCH DAMAGES. IN THE EVENT SOME JURISDICTIONS DO NOT ALLOW THE EXCLUSION OR LIMITATION OF CERTAIN DAMAGES, RELEASEES' LIABILITY IN SUCH JURISDICTIONS SHALL BE LIMITED TO THE EXTENT PERMITTED BY LAW.\n
    10. STATUTE OF LIMITATIONS: By participating in the Program, you waive any and all rights to bring any claim or action related to your participation in the Program in any forum beyond one year after the first occurrence of the act, event, condition, or omission upon which the claim or action is based.\n
    11. BINDING ARBITRATION; CLASS ACTION WAIVER: EXCEPT FOR ANY DISPUTES, CLAIMS, SUITS, ACTIONS, CAUSES OF ACTION, DEMANDS OR PROCEEDINGS (COLLECTIVELY, "DISPUTES") IN WHICH EITHER PARTY SEEKS TO BRING AN INDIVIDUAL ACTION IN SMALL CLAIMS COURT, YOU AND AEROSPOTS AGREE (A) TO WAIVE YOUR AND AEROSPORTS' RESPECTIVE RIGHTS TO HAVE ANY AND ALL DISPUTES ARISING FROM OR RELATED TO THIS AGREEMENT AND THE PROGRAM, RESOLVED IN A COURT, AND (B) TO WAIVE YOUR AND AEROSPORTS' RESPECTIVE RIGHTS TO A JURY TRIAL. INSTEAD, YOU AND AEROSPORTS AGREE TO ARBITRATE DISPUTES THROUGH BINDING ARBITRATION (WHICH IS THE REFERRAL OF A DISPUTE TO ONE OR MORE PERSONS CHARGED WITH REVIEWING THE DISPUTE AND MAKING A FINAL AND BINDING DETERMINATION TO RESOLVE IT INSTEAD OF HAVING THE DISPUTE DECIDED BY A JUDGE OR JURY IN COURT). YOU AND AEROSPORTS AGREE THAT ANY DISPUTE ARISING OUT OF OR RELATED TO THIS AGREEMENT AND THE PROGRAM IS PERSONAL TO YOU AND AEROSPORTS AND THAT SUCH DISPUTE WILL BE RESOLVED SOLELY THROUGH INDIVIDUAL ARBITRATION AND WILL NOT BE BROUGHT AS A CLASS ARBITRATION, CLASS ACTION OR ANY OTHER TYPE OF REPRESENTATIVE PROCEEDING. You and Aerosports agree that there will be no class arbitration or arbitration in which an individual attempts to resolve a Dispute as a representative of another individual or group of individuals. Further, you and Aerosports agree that a Dispute cannot be brought as a class or other type of representative action, whether within or outside of arbitration, or on behalf of any other individual or group of individuals. You and Aerosports agree that each party will notify the other party in writing of any arbitrable or small claims Dispute within thirty (30) days of the date it arises, so that the parties can attempt in good faith to resolve the Dispute informally. Notice to Aerosports shall be sent by certified mail or courier to the appropriate park. Your notice must include (a) your name, postal address, telephone number, the email address you use or used for your Program membership and, if different, an email address at which you can be contacted, (b) a description in reasonable detail of the nature or basis of the Dispute, and (c) the specific relief that you are seeking. Our notice to you will be sent electronically to the email address associated with your Program membership and will include (x) our name, postal address, telephone number and an email address at which we can be contacted with respect to the Dispute, (y) a description in reasonable detail of the nature or basis of the Dispute, and (z) the specific relief that we are seeking. If you and Aerosports cannot agree how to resolve the Dispute within thirty (30) days after the date notice is received by the applicable party, then either you or Aerosports may, as appropriate and in accordance with this Section 14, commence an arbitration proceeding or, to the extent specifically provided for in Section 14, file a claim in court. EXCEPT FOR DISPUTES IN WHICH EITHER PARTY SEEKS TO BRING AN INDIVIDUAL ACTION IN SMALL CLAIMS COURT, YOU AND AEROSPORTS AGREE THAT ANY DISPUTE MUST BE COMMENCED OR FILED BY YOU OR AEROSPORTS WITHIN ONE (1) YEAR OF THE DATE THE DISPUTE AROSE, OTHERWISE THE UNDERLYING CLAIM IS PERMANENTLY BARRED (WHICH MEANS THAT YOU AND AEROSPORTS WILL NO LONGER HAVE THE RIGHT TO ASSERT SUCH CLAIM REGARDING THE DISPUTE). You and Aerosports agree that (a) any arbitration will occur (i) in the province of Ontario, (ii) in the county where you reside, or (iii) telephonically, (b) arbitration will be conducted confidentially by a single arbitrator in accordance with Consumer Arbitration Rules that are in effect at the time the arbitration is initiated.\n
    12. GOVERNING LAW: This Agreement is governed by the laws of the province where the Aerosports park from which you purchased membership in the Program is located, without regard to the conflicts of laws rules of any jurisdiction. Any dispute, claim or cause of action arising out of or concerning the interpretation or effect of this Agreement and/or your participation in the Program, except where prohibited, shall be resolved individually, without resort to any form of class action. You agree to the personal jurisdiction, subject matter jurisdiction, and venue of these courts.\n
    13. SEVERABILITY: If any provision of this Agreement is held unenforceable or invalid under any applicable law or is so held by applicable court decision, such unenforceability or invalidity will not render this Agreement unenforceable or invalid as a whole, and such provision will be changed and interpreted so as to best accomplish the objectives of such unenforceable or invalid provision within the limits of applicable law or applicable court decisions.\n
    14. NO WAIVER: Any waiver by Aerosports of a breach by you of any provision of this Agreement shall not operate as, or be construed to be, a waiver of any other breach of such provision or of any breach by you of any other provision of this Agreement. Failure by Aerosports to insist upon strict adherence to any provision of this Agreement on one or more occasions shall not be considered a waiver or deprive Aerosports of the right to insist upon strict adherence to that provision or any other provision of this Agreement.\n
    """
    pdf.chapter_body(agreement_details)

    # Add the tick image (adjust x, y, width, and height as needed)
    pdf.image(
        resource_path("src/membership/static/tick_image.png"), x=10, y=213.5, w=7, h=7
    )  # Adjust the position (x, y) as needed

    # # Add the text "I agree to all terms and conditions" below the tick image
    pdf.set_xy(20, 212.5)  # Adjust the x, y coordinates to be aligned with the tick
    pdf.set_font("Arial", "", 12)
    pdf.cell(
        0,
        10,
        "I have read and understood the booking agreement with all terms and conditions *",
        0,
        1,
    )

    pdf.chapter_title("Signature:")

    pdf.image(data["signature"], x=10, y=None, w=0, h=40)

    return pdf

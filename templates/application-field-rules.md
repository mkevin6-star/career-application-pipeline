# Application Field Rules

Use `cv/parsed-profile.yaml` as the only source of candidate facts and `cv/search-criteria.yaml` as the only source of job-search preferences. Do not fill a field from memory, a prior employer form, or an unsupported inference.

## GREEN - May fill after employer-specific approval

Fill only when the exact verified value exists in the canonical profile:

- first and last name;
- verified job-search email and phone number;
- city, state, and country;
- university, degree, major, graduation date, and GPA;
- verified public links; and
- the user-approved resume upload.

## YELLOW - Fill only with an exact stored answer

Fill only when `cv/parsed-profile.yaml`, `cv/search-criteria.yaml`, or a user-approved reusable-answer file contains an unambiguous answer:

- desired compensation;
- relocation, travel, start date, and schedule availability;
- work authorization and sponsorship;
- prior employment with the employer;
- referral source; and
- employer-specific short answers.

If no exact answer exists, stop and ask the user. Store a new reusable answer only when the user says it may be reused.

## RED - User handles manually

Do not enter, store, or infer:

- passwords, MFA or verification codes, recovery codes, or security answers;
- CAPTCHAs and security challenges;
- SSNs, passport or government-ID numbers, banking or payment information;
- electronic signatures, attestations, consent, or authorization checkboxes;
- voluntary demographic, EEO, disability, or veteran-status questions;
- criminal-history or background-check questions; or
- any question whose meaning is unclear or whose answer is not verified.

## Always stop before external completion

- Creating an applicant account requires the user's immediate confirmation.
- Uploading a resume or other document requires explicit approval for that employer.
- Final submission is always the user's action. Mark a role `applied` only after the user confirms it was submitted.

import { FormControlLabel, Radio, RadioGroup } from '@mui/material';
import React from 'react'


const CustomGenderRadioButtonGroup = (props) => {

    const genders = [
        { id: 1, value: "female", label: "Female", isChecked: false },
        { id: 2, value: "male", label: "Male", isChecked: false },
        { id: 3, value: "other", label: "Other", isChecked: false }
    ];

    return (
        <div>
            <label>Gender</label>
            <RadioGroup row aria-label="gender" 
                onChange={(event) => props.onChange(event.target.value)}>
                {
                    genders.map((gender) => {
                        return (
                            <div>
                                { gender.isChecked = (gender.value === props.gender) && true }
                                <FormControlLabel key={gender.id} value={gender.value} control={<Radio />} label={gender.label} checked={gender.isChecked} />
                            </div>
                        )
                    })
                }
            </RadioGroup>
        </div>
    );
};

export default CustomGenderRadioButtonGroup;
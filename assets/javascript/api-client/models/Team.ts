/* tslint:disable */
/* eslint-disable */
/**
 * Investor SaaS
 * A SaaS for Investors
 *
 * The version of the OpenAPI document: 0.1.0
 * 
 *
 * NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).
 * https://openapi-generator.tech
 * Do not edit the class manually.
 */

import { exists, mapValues } from '../runtime';
import type { Invitation } from './Invitation';
import {
    InvitationFromJSON,
    InvitationFromJSONTyped,
    InvitationToJSON,
} from './Invitation';
import type { Membership } from './Membership';
import {
    MembershipFromJSON,
    MembershipFromJSONTyped,
    MembershipToJSON,
} from './Membership';
import type { PatchedTeamSubscription } from './PatchedTeamSubscription';
import {
    PatchedTeamSubscriptionFromJSON,
    PatchedTeamSubscriptionFromJSONTyped,
    PatchedTeamSubscriptionToJSON,
} from './PatchedTeamSubscription';

/**
 * 
 * @export
 * @interface Team
 */
export interface Team {
    /**
     * 
     * @type {number}
     * @memberof Team
     */
    readonly id: number;
    /**
     * 
     * @type {string}
     * @memberof Team
     */
    name: string;
    /**
     * 
     * @type {string}
     * @memberof Team
     */
    slug?: string;
    /**
     * 
     * @type {Array<Membership>}
     * @memberof Team
     */
    readonly members: Array<Membership>;
    /**
     * 
     * @type {Array<Invitation>}
     * @memberof Team
     */
    readonly invitations: Array<Invitation>;
    /**
     * 
     * @type {string}
     * @memberof Team
     */
    readonly dashboardUrl: string;
    /**
     * 
     * @type {string}
     * @memberof Team
     */
    readonly isAdmin: string;
    /**
     * 
     * @type {PatchedTeamSubscription}
     * @memberof Team
     */
    subscription: PatchedTeamSubscription;
    /**
     * 
     * @type {boolean}
     * @memberof Team
     */
    readonly hasActiveSubscription: boolean;
}

/**
 * Check if a given object implements the Team interface.
 */
export function instanceOfTeam(value: object): boolean {
    let isInstance = true;
    isInstance = isInstance && "id" in value;
    isInstance = isInstance && "name" in value;
    isInstance = isInstance && "members" in value;
    isInstance = isInstance && "invitations" in value;
    isInstance = isInstance && "dashboardUrl" in value;
    isInstance = isInstance && "isAdmin" in value;
    isInstance = isInstance && "subscription" in value;
    isInstance = isInstance && "hasActiveSubscription" in value;

    return isInstance;
}

export function TeamFromJSON(json: any): Team {
    return TeamFromJSONTyped(json, false);
}

export function TeamFromJSONTyped(json: any, ignoreDiscriminator: boolean): Team {
    if ((json === undefined) || (json === null)) {
        return json;
    }
    return {
        
        'id': json['id'],
        'name': json['name'],
        'slug': !exists(json, 'slug') ? undefined : json['slug'],
        'members': ((json['members'] as Array<any>).map(MembershipFromJSON)),
        'invitations': ((json['invitations'] as Array<any>).map(InvitationFromJSON)),
        'dashboardUrl': json['dashboard_url'],
        'isAdmin': json['is_admin'],
        'subscription': PatchedTeamSubscriptionFromJSON(json['subscription']),
        'hasActiveSubscription': json['has_active_subscription'],
    };
}

export function TeamToJSON(value?: Team | null): any {
    if (value === undefined) {
        return undefined;
    }
    if (value === null) {
        return null;
    }
    return {
        
        'name': value.name,
        'slug': value.slug,
        'subscription': PatchedTeamSubscriptionToJSON(value.subscription),
    };
}

